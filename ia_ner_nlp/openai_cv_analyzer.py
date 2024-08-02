import openai
import os
from dotenv import load_dotenv

load_dotenv()

class OpenAICVAnalyzer:
    def __init__(self):
        # Charger la clé API OpenAI à partir des variables d'environnement
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        openai.api_key = self.openai_api_key

    def interpret(self, extracted_data):
        # Préparer les données pour l'API OpenAI
        prompt = self._create_prompt(extracted_data)

        # Envoyer la requête à OpenAI
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a skilled assistant, capable of providing detailed analysis on CVs based on multiple criteria. return answer in French"},
                {"role": "user", "content": prompt}
            ],
            # max_tokens=30000
        )

        # Retourner l'analyse de l'API OpenAI
        return response.choices[0].message['content']

    def _create_prompt(self, extracted_data):
        criteria = [
            "personal_info",
            "professional_summary",
            "work_experience",
            "education",
            "skills",
            "certifications",
            "languages",
            "projects",
            "publications",
            "references",
            "hobbies"
        ]

        prompt = "Analyze the following CV data and provide a detailed score or analysis for each of the following criteria: personal_info, professional_summary, work_experience, education, skills, certifications, languages, projects, publications, references, hobbies. Include a score out of 10 for each criterion along with a detailed explanation.\n\nCV Data:\n"

        for criterion in criteria:
            data = extracted_data.get(criterion, "")
            prompt += f"\n{criterion}:\n{data}\n"

        return prompt
