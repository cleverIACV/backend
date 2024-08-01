import pdfplumber
from transformers import pipeline
import io
from PIL import Image
from resume_parser import resumeparse

# Charger le modèle de reconnaissance d'entités nommées (NER)
nlp = pipeline("ner", grouped_entities=True)

def extract_cv_data(file_path):
    extracted_data = resumeparse.read_file(file_path)

    # Lire le contenu du fichier PDF
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            extracted_data["raw_text"] = text
            for img in page.images:
                img_bbox = (img["x0"], img["top"], img["x1"], img["bottom"])
                img_obj = page.within_bbox(img_bbox).to_image()
                img_bytes = img_obj.original

                img_pil = Image.open(io.BytesIO(img_bytes))
                # Simple heuristic to detect if the image might be a photo
                if img_pil.width / img_pil.height > 0.5 and img_pil.width / img_pil.height < 2:
                    extracted_data["has_photo"] = True

    # Utiliser le modèle NER pour extraire les entités nommées
    ner_results = nlp(extracted_data["raw_text"])

    # Structurer les entités extraites
    for entity in ner_results:
        entity_type = entity["entity_group"]
        entity_text = entity["word"]
        if entity_type == "PER":
            extracted_data["personal_info"]["name"] = entity_text
        elif entity_type == "ORG":
            extracted_data["work_experience"].append({"company": entity_text})
        elif entity_type == "LOC":
            extracted_data["personal_info"]["address"] = entity_text
        # Ajouter les entités extraites aux données existantes
        extracted_data.setdefault("entities", []).append({"type": entity_type, "text": entity_text})

    return extracted_data
