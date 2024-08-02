import openai
import os
from dotenv import load_dotenv

load_dotenv()

class OpenAICoverLetterAnalyzer:
    def __init__(self):
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        openai.api_key = self.openai_api_key

    def interpret(self, extracted_data, cv_data, job_title):
        prompt = self._create_prompt(extracted_data, cv_data, job_title)

        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a skilled assistant, capable of providing detailed analysis on cover letters and CVs based on multiple criteria. Return the answer in French."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1500
        )

        return response.choices[0].message['content']

    def _create_prompt(self, extracted_data, cv_data, job_title):
        prompt = f"Analyze the following cover letter and CV data for the job title '{job_title}'. Provide detailed scores and explanations for their suitability for the job.\n\nCover Letter Data:\n{extracted_data['raw_text']}\n\nCV Data:\n{cv_data['raw_text']}"

        return prompt
