# src/gcrbot/gemini_tool.py
import os
os.environ["GRPC_VERBOSITY"] = "NONE"
os.environ["GRPC_LOG_LEVEL"] = "ERROR"
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

import google.generativeai as genai
from dotenv import load_dotenv
from gcrbot.tools.db_tool import search_pfe
import logging

# Cache les warnings Google
logging.getLogger("google.generativeai").setLevel(logging.ERROR)

# Charge la clé API
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Modèle Gemini 2.5 Flash
model = genai.GenerativeModel(
    "gemini-2.5-flash",
    system_instruction="""
    You are an expert assistant for analyzing End-of-Studies Projects (PFE).
    You use the provided data to answer factually.
    Always respond in English, using bullet points if multiple items.
    Be clear, concise, and professional.
    """
)

def ask_gemini(question: str) -> str:
    data = search_pfe(question)
    prompt = f"""
    User question: {question}
    Available data:
    {data}

    Answer in English, in a structured and professional way.
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {e}"