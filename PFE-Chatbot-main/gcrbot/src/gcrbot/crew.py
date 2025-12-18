# src/gcrbot/crew.py
import os
from dotenv import load_dotenv
from crewai import Crew, Agent, LLM, Task
from gcrbot.tools.db_tool import PFESearchTool

load_dotenv()

class InfoScolaireCrew:
    def __init__(self):
        self.tool = PFESearchTool()

        # Force Google AI Studio (pas Vertex AI)
        self.llm = LLM(
            model="gemini/gemini-1.5-pro",
            api_key=os.getenv("GOOGLE_API_KEY"),
            temperature=0.2,
            api_base="https://generativelanguage.googleapis.com/v1beta"  # ← Clé !
        )

    def info_agent(self):
        return Agent(
            role="Analyste de Projets de Fin d'Études",
            goal="Répondre précisément aux questions sur les PFE en utilisant la base CSV",
            backstory=(
                "Tu es un assistant expert en analyse de données PFE. "
                "Tu utilises l'outil de recherche pour répondre factuellement en français."
            ),
            tools=[self.tool],
            llm=self.llm,
            verbose=True,
            allow_delegation=False
        )

    def answer_question_task(self, question: str):
        return Task(
            description=f"Réponds à cette question en utilisant l'outil si nécessaire :\n{question}",
            expected_output="Réponse claire, concise et en français. Utilise des puces si plusieurs éléments.",
            agent=self.info_agent()
        )

    def run_chat(self):
        print("Chatbot InfoScolaire PFE (tape 'quit' pour quitter)")
        while True:
            q = input("\nVous : ").strip()
            if q.lower() in ['quit', 'q', 'exit']:
                print("Au revoir !")
                break
            if q:
                task = self.answer_question_task(q)
                crew = Crew(
                    agents=[self.info_agent()],
                    tasks=[task],
                    llm=self.llm,
                    verbose=True
                )
                try:
                    result = crew.kickoff()
                    print(f"\nAssistant : {result}")
                except Exception as e:
                    print(f"Erreur : {e}")

    def run(self):
        self.run_chat()