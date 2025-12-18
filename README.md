# 🎓 PFE Chatbot - AI-Powered Project Assistant (Part of project gcrbo

## 📋 Table of Contents
- [Overview](#overview)
- [Features](#features)
- [System Architecture](#system-architecture)
- [Prerequisites](#prerequisites)
- [Installation Guide](#installation-guide)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [API Endpoints](#api-endpoints)
- [Usage Examples](#usage-examples)
- [Troubleshooting](#troubleshooting)
- [Development](#development)

---

## 🌟 Overview

The **PFE Chatbot** is an intelligent assistant designed to help students discover, analyze, and compare End-of-Studies Projects (Projets de Fin d'Études). It leverages AI (Google Gemini) and provides multiple interfaces including a command-line tool, REST API, and modern web interface.

### Key Capabilities
- 🔍 Bilingual search (English/French)
- 🎯 Profile-based project recommendations
- ⚖️ Intelligent project comparison
- 📊 Analytics and statistics dashboard
- 🤖 AI-powered insights using Google Gemini

---

## ✨ Features

### 1. **Intelligent Search**
- Natural language queries in English or French
- Domain-specific filtering (AI, Cybersecurity, Web, Networking, etc.)
- Synonym recognition for broader search coverage

### 2. **Profile-Based Recommendations**
- Input your skills, certifications, and interests
- Receive personalized project suggestions
- Score-based matching algorithm

### 3. **Project Comparison** (NEW)
- Compare two projects side-by-side
- Analyze:
  - Technologies used
  - Project duration
  - Complexity level
  - Value added
  - Required tools
  - Similarity score
- Get AI-powered recommendations

### 4. **Analytics Dashboard**
- Visual statistics with interactive charts
- Projects by specialty, year, and domain
- Trend analysis and distribution views

### 5. **Topic Suggestions**
- Get curated project ideas by domain
- Based on real PFE projects database

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    User Interfaces                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   Streamlit  │  │     CLI      │  │  CrewAI      │      │
│  │   Web App    │  │   Console    │  │   Agent      │      │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘      │
└─────────┼──────────────────┼──────────────────┼─────────────┘
          │                  │                  │
          │                  ▼                  │
          │         ┌─────────────────┐         │
          └────────►│   Flask API     │◄────────┘
                    │   (Port 5000)   │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │   db_tool.py    │
                    │  Search Logic   │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │  CSV Database   │
                    │ pfe_projects.csv│
                    └─────────────────┘
                             │
                    ┌────────▼────────┐
                    │  Google Gemini  │
                    │   AI Model      │
                    └─────────────────┘
```

---

## 📦 Prerequisites

### Required Software
- **Python**: 3.10, 3.11, 3.12, or 3.13
- **pip**: Python package manager
- **Git**: For cloning the repository

### API Keys
- **Google AI Studio API Key**: Required for Gemini AI
  - Get it from: https://makersuite.google.com/app/apikey

### Operating System
- Windows 10/11
- macOS 10.15+
- Linux (Ubuntu 20.04+, Debian, etc.)

---

## 🚀 Installation Guide

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd GCRBot
```

### Step 2: Install UV (Package Manager)

UV is a fast Python package manager used by CrewAI.

**Windows:**
```bash
pip install uv
```

**macOS/Linux:**
```bash
pip install uv
# OR
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Step 3: Create Virtual Environment

```bash
# Using Python venv
python -m venv .venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate

# macOS/Linux:
source .venv/bin/activate
```

### Step 4: Install Dependencies

```bash
# Install CrewAI and dependencies
crewai install

# OR manually install packages
pip install -r requirements.txt
```

**Create `requirements.txt` if not present:**
```txt
crewai>=0.1.0
crewai-tools>=0.1.0
google-generativeai>=0.3.0
python-dotenv>=1.0.0
pandas>=2.0.0
flask>=3.0.0
flask-cors>=4.0.0
streamlit>=1.30.0
plotly>=5.18.0
requests>=2.31.0
```

### Step 5: Configure Environment Variables

Create a `.env` file in the project root:

```env
# Google AI Studio API Key
GOOGLE_API_KEY=your_google_api_key_here

# Model Configuration
model=gemini/gemini-1.5-pro
```

**To get your Google API Key:**
1. Visit https://makersuite.google.com/app/apikey
2. Click "Create API Key"
3. Copy the key and paste it in `.env`

### Step 6: Prepare Database

Ensure your CSV file is in the correct location:
```
gcrbot/
└── knowledge/
    └── pfe_projects.csv
```

**CSV Format:**
```csv
student,title,specialty,supervisor,year
"STUDENT NAME","Project Title","Specialty","Supervisor",2025
```

### Step 7: Update CSV Path (if needed)

Edit `src/gcrbot/tools/db_tool.py`:

```python
# Update this line with your actual path
CSV_PATH = Path("C:/Users/YOUR_USERNAME/Desktop/GCRBot/gcrbot/knowledge/pfe_projects.csv")

# OR use relative path
CSV_PATH = Path(__file__).parent.parent / "knowledge" / "pfe_projects.csv"
```

---

## 📁 Project Structure

```
GCRBot/
├── .env                          # Environment variables
├── .gitignore                    # Git ignore file
├── README.md                     # This file
├── pyproject.toml                # Project configuration
├── requirements.txt              # Python dependencies
├── uv.lock                       # UV lock file
│
├── gcrbot/                       # Main package (root level)
│   └── knowledge/
│       ├── pfe_projects.csv      # Projects database
│       └── user_preference.txt   # User preferences
│
└── src/
    └── gcrbot/                   # Source code
        ├── __init__.py
        ├── main.py               # CLI entry point
        ├── crew.py               # CrewAI setup
        ├── gemini_tool.py        # Gemini integration
        ├── api.py                # Flask REST API
        ├── app.py                # Streamlit web interface
        │
        ├── config/
        │   ├── agents.yaml       # Agent configurations
        │   └── tasks.yaml        # Task definitions
        │
        └── tools/
            ├── __init__.py
            ├── db_tool.py        # Database operations
            ├── custom_tool.py    # Custom tools template
            └── scrape_website_tool.py  # Web scraping (future)
```

---

## ⚙️ Configuration

### 1. Agent Configuration (`config/agents.yaml`)

```yaml
info_agent:
  role: "PFE Projects Analyst"
  goal: >
    Answer questions accurately about PFE projects using the CSV database.
  backstory: >
    You are an expert in academic data analysis.
    You use the PFE search tool to provide factual responses.
  allow_delegation: false
  verbose: true
```

### 2. Task Configuration (`config/tasks.yaml`)

```yaml
answer_question:
  description: >
    Answer the following question using the search tool if necessary:
    {{question}}
  expected_output: >
    A clear, concise response.
    If data is found, list it with bullet points.
    If nothing is found, say so politely.
  agent: info_agent
```

### 3. API Configuration

The Flask API runs on `http://127.0.0.1:5000` by default.

To change the port, edit `api.py`:
```python
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
```

### 4. Streamlit Configuration

To change the Streamlit port (default 8501):
```bash
streamlit run src/gcrbot/app.py --server.port 8502
```

---

## 🎮 Running the Application

### Method 1: Command Line Interface (CLI)

```bash
# Using CrewAI
crewai run

# OR using Python directly
python src/gcrbot/main.py
```

**Example usage:**
```
PFE Chatbot (type 'quit' to exit)

You: What are the AI projects?
Assistant: [AI projects list...]

You: Compare Wazuh project with AI Agent project
Assistant: [Comparison results...]

You: quit
Goodbye!
```

### Method 2: Flask REST API

**Start the API server:**
```bash
cd src/gcrbot
python api.py
```

The API will be available at `http://127.0.0.1:5000`

**Test the API:**
```bash
# Search query
curl -X POST http://127.0.0.1:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"question": "What are the cybersecurity projects?"}'

# Compare projects
curl -X POST http://127.0.0.1:5000/compare \
  -H "Content-Type: application/json" \
  -d '{"project1": "Wazuh", "project2": "AI Agent"}'
```

### Method 3: Streamlit Web Interface

**Start Streamlit:**
```bash
cd src/gcrbot
streamlit run app.py
```

The web interface will open automatically at `http://localhost:8501`

**For the comparison feature to work:**
1. Keep the Flask API running in one terminal
2. Run Streamlit in another terminal

---

## 🌐 API Endpoints

### 1. Search Projects
**POST** `/predict`

Request:
```json
{
  "question": "What are the AI projects?"
}
```

Response:
```json
{
  "answer": "**AI Projects Found: 3 project(s)**\n\n1. **Student:** OUESLATI DHIA EDDINE\n   **Title:** Development of a Hand Gesture-Based Cursor Control System..."
}
```

### 2. Compare Projects
**POST** `/compare`

Request:
```json
{
  "project1": "Wazuh",
  "project2": "AI Agent"
}
```

Response:
```json
{
  "project1": {
    "title": "Wazuh as SIEM and XDR...",
    "student": "TOUKEBRI OUSSAMA",
    "specialty": "Cybersecurity",
    "technologies": ["Security", "SIEM"],
    "duration": "3-4 months",
    "complexity": "Advanced",
    "value_added": "High (Enterprise-grade solution)",
    "required_skills": "Expert (Strong technical background required)",
    "tools_required": ["Wazuh/Splunk", "Kali Linux", "Wireshark"]
  },
  "project2": { ... },
  "similarity_score": 15,
  "insights": [...],
  "recommendation": "..."
}
```

### 3. Get Statistics
**GET** `/stats`

Response:
```json
{
  "total_projects": 40,
  "by_specialty": {"Cybersecurity": 5, "AI": 3, ...},
  "by_year": {"2025": 40},
  "domain_counts": {"AI/ML": 5, "Security": 8, ...},
  "specialty_percentage": {"Cybersecurity": 12.5, ...}
}
```

### 4. Topic Recommendations
**POST** `/recommend`

Request:
```json
{
  "domain": "Cybersecurity"
}
```

Response:
```json
{
  "domain": "cybersecurity",
  "suggestions": [
    "Automation of Security Incident Management...",
    "Wazuh as SIEM & XDR...",
    "Multi-Instance Vulnerability Operation Center..."
  ]
}
```

### 5. Profile-Based Recommendations
**POST** `/profile_recommend`

Request:
```json
{
  "skills": "Python, Machine Learning, Docker",
  "certifications": "AWS Cloud Practitioner",
  "interests": "AI, Cloud Computing",
  "level": "Intermediate"
}
```

Response:
```json
{
  "suggestions": [
    {
      "student": "BEN SAAD OUMAIA",
      "title": "Design and Development of an AI Agent...",
      "specialty": "AI & HR",
      "match_reasons": [
        "Matches your AI/ML skills",
        "Matches your cloud/DevOps skills"
      ]
    },
    ...
  ],
  "total_matches": 12
}
```

---

## 💡 Usage Examples

### Example 1: Simple Search

**CLI:**
```
You: Show me all blockchain projects
Assistant: **Blockchain projects:**
• ALYA MADIHA – Development of a Secure Mobile Application... (IoT & Blockchain)
• ALOUI IBTISSEM – Study and Implementation of a Blockchain-Based Solution... (Blockchain)
```

### Example 2: Bilingual Search

**CLI (French):**
```
Vous: Quels sont les projets en IA?
Assistant: **ai projects:**
• OUESLATI DHIA EDDINE – Development of a Hand Gesture-Based Cursor Control... (AI & Computer Vision)
• KHEDHER NADA – Use of Incremental Learning for Energy Disaggregation (Machine Learning)
• BEN SAAD OUMAIA – Design and Development of an AI Agent... (AI & HR)
```

### Example 3: Project Comparison

**Web Interface:**
1. Navigate to "Compare Two Projects"
2. Enter "Wazuh" in Project 1
3. Enter "AI Agent" in Project 2
4. Click "Compare Projects"
5. View:
   - Similarity score (gauge chart)
   - Side-by-side comparison
   - Technology overlap
   - Complexity comparison
   - Recommendations

### Example 4: Profile-Based Recommendation

**Web Interface:**
1. Go to "Profile-Based Recommendations"
2. Fill in:
   - Skills: "Python, TensorFlow, React"
   - Certifications: "CCNA"
   - Interests: "AI, Web Development"
   - Level: "Intermediate"
3. Click "Generate My Recommendations"
4. Get top 5 personalized project matches

---

## 🐛 Troubleshooting

### Issue 1: CSV Not Found Error

**Error:**
```
[ERROR] CSV not found: C:/Users/.../pfe_projects.csv
```

**Solution:**
1. Check if the CSV file exists at the specified path
2. Update `CSV_PATH` in `db_tool.py`:
```python
CSV_PATH = Path(__file__).parent.parent / "knowledge" / "pfe_projects.csv"
```

### Issue 2: Google API Key Error

**Error:**
```
Error: Invalid API key
```

**Solution:**
1. Verify your `.env` file contains the correct API key
2. Ensure the key starts with `AIza...`
3. Check quota limits at https://console.cloud.google.com/

### Issue 3: Flask API Connection Error (Streamlit)

**Error:**
```
❌ Cannot connect to server: Connection refused
```

**Solution:**
1. Ensure Flask API is running: `python api.py`
2. Check if port 5000 is available
3. Verify `API_BASE_URL` in `app.py` matches your Flask server

### Issue 4: Module Import Errors

**Error:**
```
ModuleNotFoundError: No module named 'crewai'
```

**Solution:**
```bash
pip install crewai crewai-tools
# OR
crewai install
```

### Issue 5: Streamlit Port Already in Use

**Error:**
```
Port 8501 is already in use
```

**Solution:**
```bash
streamlit run app.py --server.port 8502
```

### Issue 6: Project Comparison Returns 404

**Error:**
```
Project not found: 'xyz'
```

**Solution:**
- Use partial titles (keywords) instead of full titles
- Example: Use "Wazuh" instead of "Wazuh as SIEM and XDR: Evaluation and Implementation"
- Check spelling and try different keywords

---

## 🛠️ Development

### Adding New Features

#### 1. Add a New Domain to Search

Edit `db_tool.py`:
```python
domain_synonyms = {
    "ai": [...],
    "cybersecurity": [...],
    "your_new_domain": ["keyword1", "keyword2", "keyword3"]
}
```

#### 2. Add New Technology Keywords

Edit `db_tool.py` in the `TECH_KEYWORDS` dictionary:
```python
TECH_KEYWORDS = {
    "Python": ["python", "py"],
    "Your New Tech": ["keyword1", "keyword2"],
}
```

#### 3. Add New API Endpoint

Edit `api.py`:
```python
@app.route("/your_endpoint", methods=["POST"])
def your_function():
    data = request.get_json()
    # Your logic here
    return jsonify({"result": "success"})
```

#### 4. Add New Streamlit Page

Edit `app.py`:
```python
elif option == "Your New Option":
    st.subheader("Your Feature Title")
    # Your Streamlit components here
```

### Testing

#### Unit Tests (Future Implementation)

```python
# tests/test_db_tool.py
import pytest
from gcrbot.tools import db_tool

def test_load_data():
    df = db_tool.load_data()
    assert df is not None
    assert len(df) > 0

def test_extract_technologies():
    techs = db_tool.extract_technologies("AI and Machine Learning project")
    assert "AI" in techs
    assert "Machine Learning" in techs
```

Run tests:
```bash
pytest tests/
```

### Code Style

Follow PEP 8 guidelines:
```bash
# Install formatting tools
pip install black flake8

# Format code
black src/

# Check style
flake8 src/
```

---

## 📊 Database Schema

### CSV Columns

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| student | string | Student name | "DHAHRI RANIA INKO" |
| title | string | Project title | "Intelligent Marketing Print Management Platform" |
| specialty | string | Project specialty | "Computer Science" |
| supervisor | string | Project supervisor | "Dr. Smith" or "Not specified" |
| year | integer | Project year | 2025 |

### Adding New Projects

To add projects to the database:

1. Open `gcrbot/knowledge/pfe_projects.csv`
2. Add a new line following the format:
```csv
"STUDENT NAME","Project Title","Specialty","Supervisor Name",2025
```

Example:
```csv
"DOE JOHN","IoT Smart Home Automation System","IoT & Embedded Systems","Dr. Jane Smith",2025
```

---

## 🔒 Security Notes

### API Key Security
- Never commit `.env` files to version control
- Add `.env` to `.gitignore`
- Use environment variables in production
- Rotate API keys regularly

### CORS Configuration

For production, restrict CORS origins in `api.py`:
```python
from flask_cors import CORS

CORS(app, resources={
    r"/*": {
        "origins": ["https://yourdomain.com"]
    }
})
```

---

## 📝 License

This project is for educational purposes. Please respect any applicable licenses and terms of service for third-party APIs and libraries.

---

## 🤝 Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -m 'Add feature'`
4. Push to branch: `git push origin feature-name`
5. Submit a pull request

---

## 📞 Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Contact the development team
- Check the troubleshooting section

---

## 🎉 Acknowledgments

- **CrewAI** - Multi-agent framework
- **Google Gemini** - AI model
- **Streamlit** - Web interface
- **Flask** - REST API framework
- **Plotly** - Data visualization

---

## 📚 Additional Resources

- [CrewAI Documentation](https://docs.crewai.com)
- [Google AI Studio](https://makersuite.google.com)
- [Streamlit Documentation](https://docs.streamlit.io)
- [Flask Documentation](https://flask.palletsprojects.com)

---

**Last Updated:** December 2024  
**Version:** 2.0.0 (with Project Comparison Feature)
