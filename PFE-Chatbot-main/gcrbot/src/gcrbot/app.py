import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

API_BASE_URL = "http://127.0.0.1:5000"
st.set_page_config(page_title="AI-Powered PFE Assistant", layout="wide", page_icon="🎓")

# Sidebar with modern styling
st.sidebar.title("🎓 Navigation")
option = st.sidebar.selectbox(
    "Choose an option:",
    ["Search by Question", "Topic Suggestions", "Profile-Based Recommendations", "Compare Two Projects", "Analytics Dashboard"]
)

# Main title
st.title("🤖 AI-Powered PFE Assistant")
st.markdown("Discover the perfect PFE project for you with artificial intelligence")

# ---------------------------
# Option 1: Search by Question (Bilingual FR/EN)
# ---------------------------
if option == "Search by Question":
    st.subheader("💬 Ask Your Question")
    st.markdown("*Ask in French or English - the system understands both languages*")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        question = st.text_input(
            "Your question:", 
            placeholder="Ex: What are the cybersecurity projects? / Quels sont les projets en IA?"
        )
    with col2:
        st.write("")
        st.write("")
        search_btn = st.button("🔍 Search", use_container_width=True)
    
    # Example questions
    with st.expander("💡 Example Questions"):
        st.markdown("""
        - Show me all AI projects
        - Quels sont les projets blockchain?
        - How many cybersecurity projects are there?
        - List networking projects
        - Combien de projets en web?
        """)
    
    if search_btn:
        if not question:
            st.warning("⚠️ Please enter a question.")
        else:
            with st.spinner("Searching database..."):
                try:
                    response = requests.post(f"{API_BASE_URL}/predict", json={"question": question})
                    if response.status_code == 200:
                        answer = response.json().get("answer", "No results found")
                        st.success("✅ Search completed!")
                        st.markdown("### 📋 Results:")
                        st.markdown(answer)
                    else:
                        st.error(f"❌ Server error: {response.status_code}")
                except requests.exceptions.RequestException as e:
                    st.error(f"❌ Cannot connect to server: {e}")

# ---------------------------
# Option 2: Topic Suggestions
# ---------------------------
elif option == "Topic Suggestions":
    st.subheader("🎯 Suggestions by Domain")
    
    domains = ["Cybersecurity", "AI", "Blockchain", "Web", "Networking", "Mobile Networks", "Automation"]
    
    col1, col2 = st.columns([2, 1])
    with col1:
        domaine = st.selectbox("Choose a domain:", domains)
    with col2:
        st.write("")
        st.write("")
        suggest_btn = st.button("💡 Generate Suggestions", use_container_width=True)
    
    if suggest_btn:
        with st.spinner(f"Generating suggestions for {domaine}..."):
            try:
                response = requests.post(f"{API_BASE_URL}/recommend", json={"domain": domaine})
                if response.status_code == 200:
                    suggestions = response.json().get("suggestions", [])
                    if suggestions:
                        st.success(f"✅ Topics found for {domaine}")
                        st.markdown(f"### 📚 Recommended Topics:")
                        for i, s in enumerate(suggestions, 1):
                            st.markdown(f"**{i}.** {s}")
                    else:
                        st.info("ℹ️ No topics found for this domain.")
                else:
                    st.error(f"❌ Server error: {response.status_code}")
            except requests.exceptions.RequestException as e:
                st.error(f"❌ Cannot connect to server: {e}")

# ---------------------------
# Option 3: Profile-Based Recommendations
# ---------------------------
elif option == "Profile-Based Recommendations":
    st.subheader("🎯 Find THE Perfect Project for You")
    st.markdown("Fill in your profile and let AI recommend the best PFE projects")
    
    with st.form("profile_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            skills = st.text_area(
                "🛠️ Your Technical Skills",
                placeholder="Ex: Python, Machine Learning, React, Cisco, Docker...",
                height=100
            )
            
            certifications = st.text_input(
                "🏆 Your Certifications",
                placeholder="Ex: CCNA, OCI, AWS Cloud Practitioner..."
            )
        
        with col2:
            interests = st.text_area(
                "❤️ Your Interests",
                placeholder="Ex: AI, Cybersecurity, Web Development, Cloud...",
                height=100
            )
            
            level = st.selectbox(
                "📊 Your Level",
                ["Beginner", "Intermediate", "Advanced"]
            )
        
        submitted = st.form_submit_button("🚀 Generate My Recommendations", use_container_width=True)
    
    if submitted:
        if not skills and not certifications and not interests:
            st.warning("⚠️ Please fill at least one field to get recommendations.")
        else:
            with st.spinner("🔍 Analyzing your profile..."):
                try:
                    response = requests.post(
                        f"{API_BASE_URL}/profile_recommend",
                        json={
                            "skills": skills,
                            "certifications": certifications,
                            "interests": interests,
                            "level": level
                        }
                    )
                    
                    if response.status_code == 200:
                        data = response.json()
                        suggestions = data.get("suggestions", [])
                        total_matches = data.get("total_matches", 0)
                        
                        st.success(f"✅ {total_matches} projects match your profile!")
                        st.markdown("### 🎯 Top 5 Recommendations for You:")
                        
                        for i, project in enumerate(suggestions, 1):
                            with st.expander(f"**#{i} - {project.get('title', 'General Project')}**", expanded=(i==1)):
                                if 'student' in project:
                                    st.markdown(f"**👤 Student:** {project['student']}")
                                    st.markdown(f"**🏷️ Specialty:** {project['specialty']}")
                                    st.markdown(f"**📝 Title:** {project['title']}")
                                    
                                    if 'match_reasons' in project and project['match_reasons']:
                                        st.markdown("**✨ Why This Project Matches You:**")
                                        for reason in project['match_reasons']:
                                            st.markdown(f"- {reason}")
                                else:
                                    st.markdown(project.get('title', ''))
                                    if 'reasons' in project:
                                        for reason in project['reasons']:
                                            st.markdown(f"- {reason}")
                    else:
                        st.error(f"❌ Server error: {response.status_code}")
                        
                except requests.exceptions.RequestException as e:
                    st.error(f"❌ Cannot connect to server: {e}")

# ---------------------------
# NEW: Option 4 - Compare Two Projects
# ---------------------------
elif option == "Compare Two Projects":
    st.subheader("⚖️ Intelligent Project Comparison")
    st.markdown("Compare two PFE projects to help you make the best decision")
    
    col1, col2 = st.columns(2)
    
    with col1:
        project1 = st.text_input(
            "🔵 First Project Title",
            placeholder="Ex: Wazuh as SIEM",
            help="Enter keywords from the project title"
        )
    
    with col2:
        project2 = st.text_input(
            "🟢 Second Project Title",
            placeholder="Ex: AI Agent",
            help="Enter keywords from the project title"
        )
    
    # Example comparisons
    with st.expander("💡 Example Comparisons"):
        st.markdown("""
        Try comparing:
        - **Wazuh** vs **Multi-Instance VOC**
        - **AI Agent** vs **Hand Gesture**
        - **SD-WAN** vs **IaaC Platform**
        - **Blockchain** vs **IoT**
        """)
    
    compare_btn = st.button("⚖️ Compare Projects", use_container_width=True, type="primary")
    
    if compare_btn:
        if not project1 or not project2:
            st.warning("⚠️ Please enter both project titles to compare.")
        else:
            with st.spinner("🔍 Analyzing projects..."):
                try:
                    response = requests.post(
                        f"{API_BASE_URL}/compare",
                        json={"project1": project1, "project2": project2}
                    )
                    
                    if response.status_code == 200:
                        data = response.json()
                        info1 = data["project1"]
                        info2 = data["project2"]
                        similarity = data["similarity_score"]
                        insights = data["insights"]
                        recommendation = data["recommendation"]
                        
                        # Display similarity score
                        st.markdown("---")
                        st.markdown("### 📊 Similarity Score")
                        
                        col_score1, col_score2, col_score3 = st.columns([1, 2, 1])
                        with col_score2:
                            # Create a gauge chart for similarity
                            fig_gauge = go.Figure(go.Indicator(
                                mode="gauge+number",
                                value=similarity,
                                title={'text': "Similarity"},
                                gauge={
                                    'axis': {'range': [0, 100]},
                                    'bar': {'color': "darkblue"},
                                    'steps': [
                                        {'range': [0, 30], 'color': "lightgreen"},
                                        {'range': [30, 70], 'color': "yellow"},
                                        {'range': [70, 100], 'color': "lightcoral"}
                                    ],
                                    'threshold': {
                                        'line': {'color': "red", 'width': 4},
                                        'thickness': 0.75,
                                        'value': 80
                                    }
                                }
                            ))
                            fig_gauge.update_layout(height=250)
                            st.plotly_chart(fig_gauge, use_container_width=True)
                        
                        # Display projects side by side
                        st.markdown("---")
                        st.markdown("### 📋 Detailed Comparison")
                        
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.markdown("#### 🔵 Project 1")
                            st.markdown(f"**Title:** {info1['title']}")
                            st.markdown(f"**Student:** {info1['student']}")
                            st.markdown(f"**Specialty:** {info1['specialty']}")
                            st.markdown(f"**Year:** {info1['year']}")
                            
                            st.markdown("---")
                            st.markdown("**📚 Technologies:**")
                            for tech in info1['technologies']:
                                st.markdown(f"- {tech}")
                            
                            st.markdown("---")
                            st.markdown(f"**⏱️ Duration:** {info1['duration']}")
                            st.markdown(f"**🎯 Complexity:** {info1['complexity']}")
                            st.markdown(f"**💎 Value Added:** {info1['value_added']}")
                            st.markdown(f"**📊 Required Level:** {info1['required_skills']}")
                            
                            st.markdown("---")
                            st.markdown("**🛠️ Tools Required:**")
                            for tool in info1['tools_required']:
                                st.markdown(f"- {tool}")
                        
                        with col2:
                            st.markdown("#### 🟢 Project 2")
                            st.markdown(f"**Title:** {info2['title']}")
                            st.markdown(f"**Student:** {info2['student']}")
                            st.markdown(f"**Specialty:** {info2['specialty']}")
                            st.markdown(f"**Year:** {info2['year']}")
                            
                            st.markdown("---")
                            st.markdown("**📚 Technologies:**")
                            for tech in info2['technologies']:
                                st.markdown(f"- {tech}")
                            
                            st.markdown("---")
                            st.markdown(f"**⏱️ Duration:** {info2['duration']}")
                            st.markdown(f"**🎯 Complexity:** {info2['complexity']}")
                            st.markdown(f"**💎 Value Added:** {info2['value_added']}")
                            st.markdown(f"**📊 Required Level:** {info2['required_skills']}")
                            
                            st.markdown("---")
                            st.markdown("**🛠️ Tools Required:**")
                            for tool in info2['tools_required']:
                                st.markdown(f"- {tool}")
                        
                        # Display insights
                        st.markdown("---")
                        st.markdown("### 💡 Key Insights")
                        for insight in insights:
                            st.info(insight)
                        
                        # Display recommendation
                        st.markdown("---")
                        st.markdown("### 🎯 Recommendation")
                        st.success(recommendation)
                        
                        # Visual comparison charts
                        st.markdown("---")
                        st.markdown("### 📊 Visual Comparison")
                        
                        # Complexity comparison
                        complexity_map = {"Beginner": 1, "Intermediate": 2, "Advanced": 3}
                        
                        fig_comp = go.Figure()
                        fig_comp.add_trace(go.Bar(
                            name='Project 1',
                            x=['Complexity'],
                            y=[complexity_map.get(info1['complexity'], 2)],
                            marker_color='blue'
                        ))
                        fig_comp.add_trace(go.Bar(
                            name='Project 2',
                            x=['Complexity'],
                            y=[complexity_map.get(info2['complexity'], 2)],
                            marker_color='green'
                        ))
                        fig_comp.update_layout(
                            title="Complexity Comparison",
                            yaxis_title="Level",
                            yaxis=dict(tickmode='array', tickvals=[1, 2, 3], ticktext=['Beginner', 'Intermediate', 'Advanced']),
                            height=300
                        )
                        st.plotly_chart(fig_comp, use_container_width=True)
                        
                    elif response.status_code == 404:
                        error_msg = response.json().get("error", "Project not found")
                        st.error(f"❌ {error_msg}")
                        st.info("💡 Tip: Try using fewer keywords or different terms from the project title")
                    else:
                        st.error(f"❌ Server error: {response.status_code}")
                        
                except requests.exceptions.RequestException as e:
                    st.error(f"❌ Cannot connect to server: {e}")
                    st.info("Make sure the Flask API is running on http://127.0.0.1:5000")

# ---------------------------
# Option 5: Enhanced Analytics Dashboard
# ---------------------------
elif option == "Analytics Dashboard":
    st.subheader("📊 PFE Projects Analytics")
    
    try:
        with st.spinner("Loading analytics..."):
            response = requests.get(f"{API_BASE_URL}/stats")
            
        if response.status_code == 200:
            stats = response.json()
            
            # Top Metrics Row
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("📚 Total Projects", stats.get("total_projects", 0))
            with col2:
                by_specialty = stats.get("by_specialty", {})
                st.metric("🎓 Specialties", len(by_specialty))
            with col3:
                by_year = stats.get("by_year", {})
                st.metric("📅 Years Covered", len(by_year))
            with col4:
                avg = stats.get("avg_per_specialty", 0)
                st.metric("📊 Avg per Specialty", f"{avg:.1f}")
            
            st.markdown("---")
            
            # Main Charts Section
            col1, col2 = st.columns(2)
            
            # Chart 1: Projects by Specialty
            with col1:
                if by_specialty:
                    df_spec = pd.DataFrame(list(by_specialty.items()), columns=["Specialty", "Count"])
                    df_spec = df_spec.sort_values("Count", ascending=False)
                    fig1 = px.bar(
                        df_spec, 
                        x="Specialty", 
                        y="Count", 
                        color="Count",
                        text="Count",
                        title="📊 Projects by Specialty",
                        color_continuous_scale="Blues"
                    )
                    fig1.update_layout(
                        showlegend=False,
                        xaxis_title="",
                        yaxis_title="Number of Projects",
                        height=400
                    )
                    fig1.update_traces(textposition='outside')
                    st.plotly_chart(fig1, use_container_width=True)
            
            # Chart 2: Specialty Distribution (Percentage)
            with col2:
                specialty_pct = stats.get("specialty_percentage", {})
                if specialty_pct:
                    df_pct = pd.DataFrame(list(specialty_pct.items()), columns=["Specialty", "Percentage"])
                    df_pct = df_pct.sort_values("Percentage", ascending=False)
                    fig2 = px.pie(
                        df_pct, 
                        names="Specialty", 
                        values="Percentage", 
                        title="📈 Specialty Distribution (%)",
                        hole=0.4
                    )
                    fig2.update_traces(textposition='inside', textinfo='percent+label')
                    st.plotly_chart(fig2, use_container_width=True)
            
            st.markdown("---")
            
            # Secondary Charts Section
            col3, col4 = st.columns(2)
            
            # Chart 3: Domain Analysis
            with col3:
                domain_counts = stats.get("domain_counts", {})
                if domain_counts:
                    df_domain = pd.DataFrame(list(domain_counts.items()), columns=["Domain", "Count"])
                    df_domain = df_domain[df_domain['Count'] > 0].sort_values("Count", ascending=True)
                    fig3 = px.bar(
                        df_domain,
                        x="Count",
                        y="Domain",
                        orientation='h',
                        title="🔍 Projects by Technology Domain",
                        color="Count",
                        color_continuous_scale="Viridis",
                        text="Count"
                    )
                    fig3.update_layout(
                        showlegend=False,
                        xaxis_title="Number of Projects",
                        yaxis_title="",
                        height=400
                    )
                    st.plotly_chart(fig3, use_container_width=True)
            
            # Chart 4: Year Trend
            with col4:
                year_trend = stats.get("year_trend", {})
                if year_trend:
                    df_year = pd.DataFrame(list(year_trend.items()), columns=["Year", "Projects"])
                    df_year = df_year.sort_values("Year")
                    fig4 = px.line(
                        df_year,
                        x="Year",
                        y="Projects",
                        title="📅 Projects Timeline",
                        markers=True
                    )
                    fig4.update_traces(
                        line_color='#1f77b4',
                        line_width=3,
                        marker=dict(size=10)
                    )
                    fig4.update_layout(
                        xaxis_title="Year",
                        yaxis_title="Number of Projects",
                        height=400
                    )
                    st.plotly_chart(fig4, use_container_width=True)
            
            # Detailed Specialty Breakdown
            st.markdown("---")
            st.subheader("📋 Detailed Specialty Breakdown")
            if by_specialty:
                df_detail = pd.DataFrame(list(by_specialty.items()), columns=["Specialty", "Count"])
                specialty_pct_dict = stats.get("specialty_percentage", {})
                df_detail["Percentage"] = df_detail["Specialty"].map(specialty_pct_dict)
                df_detail = df_detail.sort_values("Count", ascending=False)
                df_detail.index = range(1, len(df_detail) + 1)
                
                # Format percentage
                df_detail["Percentage"] = df_detail["Percentage"].apply(lambda x: f"{x:.2f}%")
                
                st.dataframe(df_detail, use_container_width=True)
                
        else:
            st.error(f"❌ Server error: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        st.error(f"❌ Cannot connect to server: {e}")

# Footer
st.markdown("---")
st.markdown("Made with ❤️ by Your PFE Assistant")