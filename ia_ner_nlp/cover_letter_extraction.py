import pdfplumber
import spacy
import io
from PIL import Image

class CoverLetterExtractor:
    def __init__(self):
        self.spacy_nlp = spacy.load("fr_core_news_sm")

    def extract_cover_letter_data(self, file_path):
        extracted_data = {
            "raw_text": "",
            "sections": {}
        }

        # Lire le contenu du fichier PDF avec pdfplumber
        with pdfplumber.open(file_path) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text() + "\n"

        extracted_data["raw_text"] = text

        # Utiliser le modèle NER pour extraire les entités nommées
        doc = self.spacy_nlp(text)

        # Structurer les entités extraites
        for entity in doc.ents:
            entity_type = entity.label_
            entity_text = entity.text
            extracted_data.setdefault("entities", []).append({"type": entity_type, "text": entity_text})

        return extracted_data
