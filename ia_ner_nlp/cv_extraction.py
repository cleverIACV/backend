import pdfplumber
from transformers import pipeline
import io
from PIL import Image
import spacy

class CVExtractor:
    def __init__(self):
        # Charger le modèle de reconnaissance d'entités nommées (NER)
        self.ner_pipeline = pipeline("ner", model="Jean-Baptiste/roberta-large-ner-english", aggregation_strategy="simple")
        self.spacy_nlp = spacy.load("fr_core_news_sm")

    def extract_cv_data(self, file_path):
        extracted_data = {
            "raw_text": "",
            "has_photo": False,
            "personal_info": {},
            "professional_summary": "",
            "work_experience": [],
            "education": [],
            "skills": [],
            "certifications": [],
            "languages": [],
            "projects": [],
            "publications": [],
            "references": [],
            "hobbies": [],
            "sections": {}
        }

        # Lire le contenu du fichier PDF avec pdfminer
        with open(file_path, "rb") as f:
            text = f.read().decode("utf-8", errors="ignore")
        extracted_data["raw_text"] = text

        # Lire les images du fichier PDF avec pdfplumber
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                for img in page.images:
                    img_bbox = (img["x0"], img["top"], img["x1"], img["bottom"])
                    img_obj = page.within_bbox(img_bbox).to_image()
                    img_bytes = img_obj.resolve()  # Utiliser .resolve() pour obtenir les bytes de l'image

                    img_pil = Image.open(io.BytesIO(img_bytes))
                    # Simple heuristic to detect if the image might be a photo
                    if img_pil.width / img_pil.height > 0.5 and img_pil.width / img_pil.height < 2:
                        extracted_data["has_photo"] = True

        # Utiliser le modèle NER pour extraire les entités nommées
        ner_results = self.ner_pipeline(extracted_data["raw_text"])

        # Structurer les entités extraites
        for entity in ner_results:
            entity_type = entity["entity_group"]
            entity_text = entity["word"]
            if entity_type == "PER":
                extracted_data.setdefault("personal_info", {}).setdefault("name", entity_text)
            elif entity_type == "ORG":
                extracted_data.setdefault("work_experience", []).append({"company": entity_text})
            elif entity_type == "LOC":
                extracted_data.setdefault("personal_info", {}).setdefault("address", entity_text)
            # Ajouter les entités extraites aux données existantes
            extracted_data.setdefault("entities", []).append({"type": entity_type, "text": entity_text})

        return extracted_data
