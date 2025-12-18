# src/gcrbot/tools/db_tool.py
import pandas as pd
from pathlib import Path
from collections import Counter

# Absolute path to CSV
CSV_PATH = Path("C:/Users/naffe/OneDrive/Desktop/GCRBot/gcrbot/knowledge/pfe_projects.csv")
_df = None

def load_data():
    global _df
    if _df is not None:
        return _df

    if not CSV_PATH.exists():
        print(f"[ERROR] CSV not found: {CSV_PATH}")
        return None

    _df = pd.read_csv(CSV_PATH)
    _df['title_lower'] = _df['title'].str.lower()
    _df['specialty_lower'] = _df['specialty'].str.lower()
    return _df

# ============================================
# COMPARISON FEATURE - NEW FUNCTIONS
# ============================================

TECH_KEYWORDS = {
    "Python": ["python", "py"],
    "Machine Learning": ["ml", "machine learning", "deep learning", "incremental learning"],
    "AI": ["ai", "intelligence artificielle", "artificial intelligence", "intelligent"],
    "Web": ["django", "react", "angular", "web", "spring boot", "platform"],
    "Security": ["wazuh", "siem", "soar", "cyber", "pentest", "security", "firewall", "fortinet", "palo alto"],
    "Networking": ["eigrp", "ospf", "network", "routing", "sd-wan", "cisco", "meraki"],
    "Mobile Networks": ["4g", "5g", "telecommunications", "ftto", "ftta"],
    "Cloud": ["oci", "aws", "gcp", "cloud", "docker", "kubernetes"],
    "IaaC": ["iaac", "terraform", "orchestration", "infrastructure as code"],
    "Blockchain": ["blockchain", "iota", "dlc", "distributed ledger"],
    "IoT": ["iot", "internet of things", "embedded", "sensor"],
    "Automation": ["automation", "automated", "automate"],
    "Computer Vision": ["ocr", "image processing", "computer vision", "gesture"],
    "Quality Assurance": ["testing", "quality", "qa", "qos"]
}

def extract_technologies(text):
    """Extract technologies from project title"""
    text = text.lower()
    used = []
    
    for tech, keywords in TECH_KEYWORDS.items():
        if any(k in text for k in keywords):
            used.append(tech)
    
    return used if used else ["General IT"]

def estimate_duration(title):
    """Estimate project duration based on keywords"""
    t = title.lower()
    
    # Long duration projects (4-5 months)
    if any(k in t for k in ["deep learning", "intelligent", "optimization", "design and implementation", "multi-instance"]):
        return "4-5 months"
    
    # Medium-long duration (3-4 months)
    if any(k in t for k in ["ai", "machine learning", "siem", "soar", "orchestration", "iaac platform"]):
        return "3-4 months"
    
    # Medium duration (2-3 months)
    if any(k in t for k in ["web", "platform", "mobile application", "blockchain", "automation"]):
        return "2-3 months"
    
    # Short duration (1-2 months)
    if any(k in t for k in ["study", "analysis", "testing", "generator", "interface"]):
        return "1-2 months"
    
    return "2-3 months"  # Default

def estimate_complexity(title, specialty):
    """Estimate project complexity"""
    t = (title + " " + specialty).lower()
    
    # Advanced complexity
    advanced_keywords = [
        "deep learning", "ai agent", "intelligent", "optimization", 
        "orchestration", "multi-instance", "distributed", "blockchain",
        "iaac platform", "siem", "soar", "sd-wan architecture"
    ]
    
    if any(k in t for k in advanced_keywords):
        return "Advanced"
    
    # Intermediate complexity
    intermediate_keywords = [
        "implementation", "deployment", "automation", "platform",
        "web development", "network security", "machine learning",
        "mobile application", "integration"
    ]
    
    if any(k in t for k in intermediate_keywords):
        return "Intermediate"
    
    # Beginner complexity
    return "Beginner"

def estimate_value_added(title, specialty):
    """Estimate value added by the project"""
    t = (title + " " + specialty).lower()
    
    # Very High Value
    if any(k in t for k in ["automation", "ai", "intelligent", "optimization", "orchestration"]):
        return "Very High (Innovation + Automation)"
    
    # High Value
    if any(k in t for k in ["security", "siem", "cloud", "iaac", "blockchain", "quality"]):
        return "High (Enterprise-grade solution)"
    
    # Medium Value
    if any(k in t for k in ["platform", "web", "mobile", "management", "monitoring"]):
        return "Medium (Business solution)"
    
    return "Moderate (Learning project)"

def estimate_required_skills(title, specialty):
    """Estimate required skill level"""
    complexity = estimate_complexity(title, specialty)
    
    if complexity == "Advanced":
        return "Expert (Strong technical background required)"
    elif complexity == "Intermediate":
        return "Intermediate (Good fundamentals required)"
    else:
        return "Beginner (Basic knowledge sufficient)"

def get_tools_required(technologies):
    """Get tools required based on technologies"""
    tools = set()
    
    tech_to_tools = {
        "Python": ["Python 3.x", "VS Code/PyCharm"],
        "Machine Learning": ["TensorFlow/PyTorch", "Jupyter Notebook", "scikit-learn"],
        "AI": ["TensorFlow/Keras", "OpenCV (if vision)", "Google Colab"],
        "Web": ["Node.js/npm", "React/Angular CLI", "Postman"],
        "Security": ["Wazuh/Splunk", "Kali Linux", "Wireshark"],
        "Networking": ["Cisco Packet Tracer", "GNS3", "Wireshark"],
        "Mobile Networks": ["Network simulators", "Spectrum analyzers"],
        "Cloud": ["Docker", "AWS/GCP account", "Terraform"],
        "IaaC": ["Terraform", "Ansible", "Git"],
        "Blockchain": ["Solidity", "Web3.js", "MetaMask"],
        "IoT": ["Arduino IDE", "Raspberry Pi", "MQTT broker"],
        "Automation": ["Python", "Ansible", "Jenkins/GitLab CI"],
        "Computer Vision": ["OpenCV", "TensorFlow", "Python"],
        "Quality Assurance": ["Selenium", "JUnit/TestNG", "Postman"]
    }
    
    for tech in technologies:
        if tech in tech_to_tools:
            tools.update(tech_to_tools[tech])
    
    if not tools:
        tools.add("Standard IDE")
        tools.add("Git")
    
    return list(tools)

def calculate_similarity_score(project1_info, project2_info):
    """Calculate similarity score between two projects"""
    score = 0
    
    # Technology overlap
    tech1 = set(project1_info["technologies"])
    tech2 = set(project2_info["technologies"])
    tech_overlap = len(tech1.intersection(tech2))
    score += tech_overlap * 10
    
    # Same specialty
    if project1_info["specialty"] == project2_info["specialty"]:
        score += 15
    
    # Similar complexity
    if project1_info["complexity"] == project2_info["complexity"]:
        score += 10
    
    # Similar duration
    if project1_info["duration"] == project2_info["duration"]:
        score += 5
    
    return min(score, 100)  # Cap at 100

def get_project_comparison_info(title):
    """Get detailed information about a project for comparison"""
    df = load_data()
    if df is None:
        return None
    
    title_lower = title.lower()
    mask = df["title_lower"].str.contains(title_lower, case=False, na=False)
    
    if not mask.any():
        return None
    
    row = df[mask].iloc[0]
    technologies = extract_technologies(row["title"])
    
    info = {
        "title": str(row["title"]),
        "student": str(row["student"]),
        "specialty": str(row["specialty"]),
        "year": int(row["year"]) if pd.notna(row["year"]) else 0,  # Convert to native Python int
        "technologies": technologies,
        "duration": estimate_duration(row["title"]),
        "complexity": estimate_complexity(row["title"], row["specialty"]),
        "value_added": estimate_value_added(row["title"], row["specialty"]),
        "required_skills": estimate_required_skills(row["title"], row["specialty"]),
        "tools_required": get_tools_required(technologies)
    }
    
    return info

# ============================================
# ORIGINAL SEARCH FUNCTION
# ============================================

def search_pfe(query: str) -> str:
    df = load_data()
    if df is None:
        return "Database unavailable."

    q = query.lower()
    results = []

    # Domain synonyms dictionary
    domain_synonyms = {
        "ai": ["ai", "ia", "intelligence artificielle", "artificial intelligence", "machine learning", "deep learning"],
        "blockchain": ["blockchain", "iota", "crypto", "dlc"],
        "cybersecurity": ["cybersecurity", "cyber security", "cybersécurité", "cyber-sécurité", "sécurité informatique", "security"],
        "network security": ["network security", "sécurité réseau", "networking"],
        "web": ["web", "web development", "développement web"],
        "iot": ["iot", "internet of things", "iota"],
        "automation": ["automation", "automatisation", "process optimization"],
        "mobile networks": ["mobile networks", "4g", "5g", "mobile"],
        "image processing": ["image processing", "computer vision", "cv"],
        "software quality": ["quality", "software quality", "testing", "qa"],
    }

    # Check by domain
    matched = False
    for domain, synonyms in domain_synonyms.items():
        if any(k in q for k in synonyms):
            mask = df['title_lower'].str.contains('|'.join(synonyms), case=False, na=False) | \
                   df['specialty_lower'].str.contains('|'.join(synonyms), case=False, na=False)
            projects = df[mask]
            if not projects.empty:
                results.append(f"**{domain.capitalize()} projects:**")
                for _, row in projects.iterrows():
                    results.append(f"• **{row['student']}** – {row['title']} ({row['specialty']})")
            else:
                results.append(f"No {domain} projects found.")
            matched = True
            break

    # Fallback: full scan
    if not matched:
        mask = df['title_lower'].str.contains(q, case=False, na=False) | \
               df['specialty_lower'].str.contains(q, case=False, na=False)
        projects = df[mask]
        if not projects.empty:
            results.append("**Matching projects:**")
            for _, row in projects.iterrows():
                results.append(f"• **{row['student']}** – {row['title']} ({row['specialty']})")
        else:
            results.append("No matching projects found.")

    return "\n".join(results) if results else "No relevant information found."