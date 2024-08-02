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
        with pdfplumber.open(file_path) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text() + "\n"
                for img in page.images:
                    img_bbox = (img["x0"], img["top"], img["x1"], img["bottom"])
                    img_obj = page.within_bbox(img_bbox).to_image()
                    img_pil = img_obj.original  # Extraire l'image PIL

                    # Convertir l'image PIL en bytes
                    img_byte_arr = io.BytesIO()
                    img_pil.save(img_byte_arr, format="PNG")  # Utiliser le format "PNG" explicitement
                    img_bytes = img_byte_arr.getvalue()

                    # Simple heuristic to detect if the image might be a photo
                    if img_pil.width / img_pil.height > 0.5 and img_pil.width / img_pil.height < 2:
                        extracted_data["has_photo"] = True

        extracted_data["raw_text"] = text

        # Utiliser le modèle NER pour extraire les entités nommées
        ner_results = self.ner_pipeline(text)

        # Initialiser les sections pour l'extraction des informations
        current_section = None

        # Analyser les lignes de texte
        lines = text.split("\n")
        for line in lines:
            line = line.strip()
            if not line:
                continue

            # Détecter les sections par mots-clés
            if "expérience professionnelle" in line.lower():
                current_section = "work_experience"
            elif "formation" in line.lower() or "éducation" in line.lower():
                current_section = "education"
            elif "compétences" in line.lower():
                current_section = "skills"
            elif "certifications" in line.lower():
                current_section = "certifications"
            elif "langues" in line.lower():
                current_section = "languages"
            elif "projets" in line.lower():
                current_section = "projects"
            elif "publications" in line.lower():
                current_section = "publications"
            elif "références" in line.lower():
                current_section = "references"
            elif "loisirs" in line.lower() or "hobbies" in line.lower():
                current_section = "hobbies"
            else:
                # Ajouter le texte à la section actuelle
                if current_section:
                    extracted_data[current_section].append(line)
                else:
                    # Si aucune section n'est détectée, ajouter au résumé professionnel
                    extracted_data["professional_summary"] += line + " "

        # Structurer les entités extraites
        for entity in ner_results:
            entity_type = entity["entity_group"]
            entity_text = entity["word"]
            if entity_type == "PER":
                extracted_data.setdefault("personal_info", {})["name"] = entity_text
            elif entity_type == "ORG":
                extracted_data.setdefault("work_experience", []).append({"company": entity_text})
            elif entity_type == "LOC":
                extracted_data.setdefault("personal_info", {})["address"] = entity_text
            # Ajouter les entités extraites aux données existantes
            extracted_data.setdefault("entities", []).append({"type": entity_type, "text": entity_text})

        return extracted_data
