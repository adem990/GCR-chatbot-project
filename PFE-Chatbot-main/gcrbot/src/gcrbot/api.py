import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

from flask import Flask, request, jsonify
from tools import db_tool
import pandas as pd
import re

app = Flask(__name__)

# ---------------------------
# Enhanced bilingual search with professional output
# ---------------------------
@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    if not data or "question" not in data:
        return jsonify({"error": "Missing 'question'"}), 400
    
    question = data["question"].lower()
    
    # Load database
    df = db_tool.load_data()
    if df is None:
        return jsonify({"answer": "Database currently unavailable. Please try again later."}), 500
    
    # Bilingual keyword mapping (French/English)
    keyword_mappings = {
        "ai": ["ai", "ia", "intelligence artificielle", "artificial intelligence", "machine learning", "deep learning", "ml"],
        "cybersecurity": ["cybersecurity", "cyber security", "cybersécurité", "cyber-sécurité", "sécurité", "security", "siem", "soar", "pentest"],
        "blockchain": ["blockchain", "iota", "crypto", "dlc", "distributed ledger"],
        "network": ["network", "réseau", "networking", "sd-wan", "cisco", "routing"],
        "web": ["web", "website", "site web", "platform", "plateforme", "angular", "react", "spring"],
        "iot": ["iot", "internet of things", "internet des objets", "embedded"],
        "automation": ["automation", "automatisation", "automate", "automated"],
        "mobile": ["mobile", "4g", "5g", "telecommunications", "télécommunications"],
        "cloud": ["cloud", "iaac", "devops", "orchestration", "terraform"],
        "quality": ["quality", "qualité", "testing", "qa", "test"]
    }
    
    # Detect domain from question
    detected_domain = None
    for domain, keywords in keyword_mappings.items():
        if any(keyword in question for keyword in keywords):
            detected_domain = domain
            break
    
    # Build response
    results = []
    
    if detected_domain:
        # Search using all synonyms for the detected domain
        search_terms = keyword_mappings[detected_domain]
        pattern = '|'.join(search_terms)
        
        mask = df['title_lower'].str.contains(pattern, case=False, na=False, regex=True) | \
               df['specialty_lower'].str.contains(pattern, case=False, na=False, regex=True)
        
        projects = df[mask]
        
        if not projects.empty:
            results.append(f"**{detected_domain.upper()} Projects Found: {len(projects)} project(s)**\n")
            
            for idx, (_, row) in enumerate(projects.iterrows(), 1):
                results.append(f"{idx}. **Student:** {row['student']}")
                results.append(f"   **Title:** {row['title']}")
                results.append(f"   **Specialty:** {row['specialty']}")
                results.append(f"   **Year:** {row['year']}\n")
        else:
            results.append(f"No {detected_domain} projects found in the database.")
    
    # Handle "how many" questions
    elif any(phrase in question for phrase in ["how many", "combien", "number of", "nombre de"]):
        if any(word in question for word in ["total", "tous", "all", "projects", "projets"]):
            total = len(df)
            results.append(f"**Total Projects:** {total}")
        elif any(word in question for word in ["specialty", "specialties", "spécialité", "spécialités"]):
            specialty_counts = df['specialty'].value_counts()
            results.append("**Projects by Specialty:**\n")
            for spec, count in specialty_counts.items():
                results.append(f"• {spec}: {count} project(s)")
        else:
            # Try to find specialty name in question
            for specialty in df['specialty'].unique():
                if specialty.lower() in question:
                    count = len(df[df['specialty'] == specialty])
                    results.append(f"**{specialty}:** {count} project(s)")
                    break
    
    # Handle "list" or "show" questions
    elif any(word in question for word in ["list", "show", "liste", "affiche", "display"]):
        if any(word in question for word in ["all", "tous", "everything"]):
            results.append(f"**All Projects ({len(df)} total):**\n")
            for idx, (_, row) in enumerate(df.iterrows(), 1):
                results.append(f"{idx}. {row['student']} - {row['title']} ({row['specialty']})")
                if idx >= 20:  # Limit to first 20 for readability
                    results.append(f"\n... and {len(df) - 20} more projects")
                    break
    
    # Fallback: general keyword search
    else:
        # Extract potential search terms (remove common words)
        stopwords = ["what", "is", "are", "the", "a", "an", "in", "on", "for", "with", "about",
                     "quel", "quelle", "est", "sont", "le", "la", "les", "un", "une", "dans", "sur", "pour"]
        search_words = [w for w in question.split() if w not in stopwords and len(w) > 3]
        
        if search_words:
            pattern = '|'.join(search_words)
            mask = df['title_lower'].str.contains(pattern, case=False, na=False, regex=True) | \
                   df['specialty_lower'].str.contains(pattern, case=False, na=False, regex=True) | \
                   df['student'].str.lower().str.contains(pattern, case=False, na=False, regex=True)
            
            projects = df[mask]
            
            if not projects.empty:
                results.append(f"**Search Results: {len(projects)} project(s) found**\n")
                for idx, (_, row) in enumerate(projects.iterrows(), 1):
                    results.append(f"{idx}. **Student:** {row['student']}")
                    results.append(f"   **Title:** {row['title']}")
                    results.append(f"   **Specialty:** {row['specialty']}")
                    results.append(f"   **Year:** {row['year']}\n")
            else:
                results.append("No matching projects found. Please try different keywords.")
        else:
            results.append("Please provide more specific search terms (e.g., AI, cybersecurity, blockchain, web, networking).")
    
    final_answer = "\n".join(results) if results else "No relevant information found. Please refine your query."
    return jsonify({"answer": final_answer})

@app.route("/recommend", methods=["POST"])
def recommend_topic():
    data = request.get_json()
    if not data or "domain" not in data:
        return jsonify({"error": "Missing 'domain'"}), 400

    domain = data["domain"].lower()
    suggestions = {
        "cybersecurity": [
            "Automation of Security Incident Management in Microsoft 365 with SIEM/SOAR",
            "Wazuh as SIEM & XDR: Evaluation and Implementation",
            "Multi-Instance Vulnerability Operation Center (VOC)"
        ],
        "ai": [
            "Development of a Hand Gesture-Based Cursor Control System Using AI",
            "Use of Incremental Learning for Energy Disaggregation",
            "AI Agent for HR Process Automation"
        ],
        "blockchain": [
            "Development of Secure Mobile Application with IoT & Blockchain",
            "Blockchain-Based Solution for Internship Certificates"
        ],
        "web": [
            "Internal Company Website",
            "Co-Working Space Booking Platform (Spring Boot + Angular)",
            "Management Website with Generative AI Solutions"
        ]
    }

    topics = suggestions.get(domain, ["No predefined suggestions for this domain."])
    return jsonify({"domain": domain, "suggestions": topics})

# ---------------------------
# Enhanced stats with more dashboards
# ---------------------------
@app.route("/stats", methods=["GET"])
def stats():
    df = db_tool.load_data()
    if df is None:
        return jsonify({"error": "Database unavailable"}), 500

    # Basic counts
    total_projects = len(df)
    by_specialty = df['specialty'].value_counts().to_dict()
    by_year = df['year'].value_counts().to_dict()
    
    # Additional analytics
    # 1. Top students with most projects
    by_student = df['student'].value_counts().head(10).to_dict()
    
    # 2. Projects per year trend
    year_trend = df.groupby('year').size().to_dict()
    
    # 3. Specialty distribution percentage
    specialty_percentage = (df['specialty'].value_counts() / total_projects * 100).round(2).to_dict()
    
    # 4. Average projects per specialty
    avg_per_specialty = len(df) / len(df['specialty'].unique())
    
    # 5. Domain keywords analysis
    domain_counts = {}
    keywords = {
        "AI/ML": ["ai", "machine learning", "intelligent", "learning"],
        "Security": ["security", "cyber", "siem"],
        "Network": ["network", "sd-wan", "routing"],
        "Web": ["web", "platform", "website"],
        "Automation": ["automation", "automated"],
        "Cloud": ["cloud", "iaac", "orchestration"],
        "Blockchain": ["blockchain", "iota"],
        "IoT": ["iot", "embedded"]
    }
    
    for domain, terms in keywords.items():
        pattern = '|'.join(terms)
        count = df['title_lower'].str.contains(pattern, case=False, na=False, regex=True).sum()
        domain_counts[domain] = int(count)

    stats = {
        "total_projects": total_projects,
        "by_specialty": by_specialty,
        "by_year": by_year,
        "by_student": by_student,
        "specialty_percentage": specialty_percentage,
        "avg_per_specialty": round(avg_per_specialty, 2),
        "domain_counts": domain_counts,
        "year_trend": year_trend
    }
    
    return jsonify(stats)

# ---------------------------
# Profile-based recommendation
# ---------------------------
@app.route("/profile_recommend", methods=["POST"])
def profile_recommend():
    data = request.get_json()
    
    skills = data.get("skills", "").lower()
    certifications = data.get("certifications", "").lower()
    interests = data.get("interests", "").lower()
    level = data.get("level", "").lower()
    
    df = db_tool.load_data()
    if df is None:
        return jsonify({"error": "Database unavailable"}), 500
    
    project_scores = []
    
    for idx, row in df.iterrows():
        score = 0
        reasons = []
        title_lower = row['title'].lower()
        specialty_lower = row['specialty'].lower()
        
        # AI/ML matching
        if any(k in skills for k in ["python", "ml", "machine learning", "deep learning", "ai"]) or "ai" in interests:
            if any(k in title_lower or k in specialty_lower for k in ["ai", "machine learning", "intelligent", "learning"]):
                score += 3
                reasons.append("Matches your AI/ML skills")
        
        # Networking matching
        if any(k in skills for k in ["network", "routing", "switching", "cisco", "sd-wan"]) or "ccna" in certifications or "networking" in interests:
            if any(k in title_lower or k in specialty_lower for k in ["network", "sd-wan", "routing", "cisco"]):
                score += 3
                reasons.append("Matches your networking expertise")
        
        # Cybersecurity matching
        if any(k in skills for k in ["security", "cyber", "siem", "soar", "pentest"]) or "cybersecurity" in interests:
            if any(k in title_lower or k in specialty_lower for k in ["security", "cyber", "siem", "soar"]):
                score += 3
                reasons.append("Matches your security skills")
        
        # Web development matching
        if any(k in skills for k in ["web", "html", "react", "angular", "django", "spring"]) or "web" in interests:
            if any(k in title_lower or k in specialty_lower for k in ["web", "platform", "angular", "spring"]):
                score += 3
                reasons.append("Matches your web development skills")
        
        # Cloud/DevOps matching
        if any(k in skills for k in ["cloud", "devops", "docker", "kubernetes", "terraform"]) or any(k in certifications for k in ["oci", "aws", "azure"]):
            if any(k in title_lower or k in specialty_lower for k in ["iaac", "cloud", "orchestr", "automation"]):
                score += 3
                reasons.append("Matches your cloud/DevOps skills")
        
        # Blockchain matching
        if any(k in skills for k in ["blockchain", "iota", "crypto"]) or "blockchain" in interests:
            if any(k in title_lower or k in specialty_lower for k in ["blockchain", "iota"]):
                score += 3
                reasons.append("Matches your blockchain interest")
        
        # IoT matching
        if any(k in skills for k in ["iot", "embedded", "sensor"]) or "iot" in interests:
            if any(k in title_lower or k in specialty_lower for k in ["iot", "embedded"]):
                score += 3
                reasons.append("Matches your IoT skills")
        
        # Automation matching
        if any(k in skills for k in ["automation", "scripting", "ansible"]) or "automation" in interests:
            if any(k in title_lower or k in specialty_lower for k in ["automation", "automated"]):
                score += 3
                reasons.append("Matches your automation skills")
        
        # Level adjustment
        complexity_keywords = ["implementation", "design", "optimization", "intelligent", "advanced"]
        is_complex = any(k in title_lower for k in complexity_keywords)
        
        if level == "beginner" and not is_complex:
            score += 1
        elif level == "advanced" and is_complex:
            score += 1
        elif level == "intermediate":
            score += 0.5
        
        if score > 0:
            project_scores.append({
                "student": row['student'],
                "title": row['title'],
                "specialty": row['specialty'],
                "score": score,
                "reasons": reasons
            })
    
    project_scores.sort(key=lambda x: x['score'], reverse=True)
    top_projects = project_scores[:5]
    
    if not top_projects:
        suggestions = [
            {
                "title": "General software development project adapted to your profile",
                "reasons": ["Based on your general interests"]
            }
        ]
    else:
        suggestions = [
            {
                "student": p['student'],
                "title": p['title'],
                "specialty": p['specialty'],
                "match_reasons": p['reasons']
            }
            for p in top_projects
        ]
    
    return jsonify({
        "suggestions": suggestions,
        "total_matches": len(project_scores)
    })

# ---------------------------
# NEW: Project Comparison Endpoint
# ---------------------------
@app.route("/compare", methods=["POST"])
def compare_projects():
    """
    Compare two PFE projects with intelligent analysis
    """
    data = request.get_json()
    
    if not data or "project1" not in data or "project2" not in data:
        return jsonify({"error": "Missing 'project1' or 'project2' in request"}), 400
    
    project1_query = data["project1"].strip()
    project2_query = data["project2"].strip()
    
    if not project1_query or not project2_query:
        return jsonify({"error": "Project titles cannot be empty"}), 400
    
    # Get detailed information for both projects
    info1 = db_tool.get_project_comparison_info(project1_query)
    info2 = db_tool.get_project_comparison_info(project2_query)
    
    # Check if projects were found
    if info1 is None:
        return jsonify({"error": f"Project 1 not found: '{project1_query}'"}), 404
    
    if info2 is None:
        return jsonify({"error": f"Project 2 not found: '{project2_query}'"}), 404
    
    # Calculate similarity score
    similarity_score = db_tool.calculate_similarity_score(info1, info2)
    
    # Generate intelligent insights
    insights = []
    
    # Technology overlap analysis
    tech1 = set(info1["technologies"])
    tech2 = set(info2["technologies"])
    common_tech = tech1.intersection(tech2)
    
    if common_tech:
        insights.append(f"✅ Both projects share {len(common_tech)} common technology/technologies: {', '.join(common_tech)}")
    else:
        insights.append("⚠️ These projects use completely different technology stacks")
    
    # Specialty comparison
    if info1["specialty"] == info2["specialty"]:
        insights.append(f"✅ Both projects are from the same specialty: {info1['specialty']}")
    else:
        insights.append(f"📊 Different specialties: Project 1 ({info1['specialty']}) vs Project 2 ({info2['specialty']})")
    
    # Complexity comparison
    if info1["complexity"] == info2["complexity"]:
        insights.append(f"⚖️ Both projects have similar complexity: {info1['complexity']}")
    elif info1["complexity"] == "Advanced" or info2["complexity"] == "Advanced":
        insights.append("⚠️ One project is significantly more complex than the other")
    
    # Duration comparison
    if info1["duration"] == info2["duration"]:
        insights.append(f"⏱️ Similar time commitment: {info1['duration']}")
    else:
        insights.append(f"⏱️ Different durations: Project 1 ({info1['duration']}) vs Project 2 ({info2['duration']})")
    
    # Generate recommendation
    recommendation = generate_recommendation(info1, info2, similarity_score)
    
    return jsonify({
        "project1": info1,
        "project2": info2,
        "similarity_score": round(similarity_score, 2),
        "insights": insights,
        "recommendation": recommendation
    })

def generate_recommendation(info1, info2, similarity_score):
    """
    Generate an intelligent recommendation based on project comparison
    """
    recommendations = []
    
    if similarity_score > 70:
        recommendations.append("⚠️ These projects are very similar. Consider choosing one based on your specific interests.")
    elif similarity_score < 30:
        recommendations.append("✅ These projects offer very different experiences - great for diversification!")
    else:
        recommendations.append("📊 These projects have some overlap but distinct focuses.")
    
    # Complexity-based recommendation
    if info1["complexity"] == "Beginner" and info2["complexity"] == "Advanced":
        recommendations.append("💡 Project 1 is better for beginners, while Project 2 requires advanced skills.")
    elif info1["complexity"] == "Advanced" and info2["complexity"] == "Beginner":
        recommendations.append("💡 Project 2 is better for beginners, while Project 1 requires advanced skills.")
    elif info1["complexity"] == info2["complexity"] == "Advanced":
        recommendations.append("🎯 Both projects are challenging - ensure you have the required skills.")
    
    # Value-based recommendation
    if "Very High" in info1["value_added"]:
        recommendations.append(f"⭐ Project 1 offers exceptional value: {info1['value_added']}")
    if "Very High" in info2["value_added"]:
        recommendations.append(f"⭐ Project 2 offers exceptional value: {info2['value_added']}")
    
    return " ".join(recommendations)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)