# RH Recrutement: Analyse de C.V. et Lettre de Motivation

## Présentation du Projet

Ce projet est conçu pour automatiser le processus de recrutement en analysant les CVs et les lettres de motivation. Il utilise des techniques avancées de traitement du langage naturel (NLP) pour extraire des informations pertinentes et les structurer de manière à faciliter le travail des recruteurs.

## Fonctionnalités Développées

- **Extraction de Texte** : Utilisation de pdfplumber pour extraire le texte brut des CVs au format PDF.
- **Détection de Photos** : Identification des photos dans les CVs en utilisant des heuristiques basées sur les dimensions des images.
- **Reconnaissance d'Entités Nommées (NER)** : Utilisation de modèles de reconnaissance d'entités nommées pour identifier les informations personnelles et professionnelles (nom, entreprises, adresses, etc.).
- **Segmentation du CV** : Détection et segmentation des sections du CV (expérience professionnelle, formation, compétences, etc.).
- **Structuration des Données** : Organisation des données extraites en un format structuré pour faciliter l'analyse.
- **Interface Front-End** : Interface utilisateur développée en Vue.js pour visualiser et interagir avec les données extraites.
- **API REST** : Backend développé en Python, fournissant des endpoints pour l'analyse des CVs et la gestion des données.

## Démarrage du Projet via Docker

### Prérequis

- Docker installé sur votre machine.

### Instructions

1. **Cloner le dépôt du projet**:
   ```bash
   git clone https://github.com/cleverIACV/backend.git
   cd backend
   ```

2. **Construire l'image Docker**:
   ```bash
    docker build -t rh-recrutement .
    ```

3. **Cloner le dépôt du projet**:
   ```bash
    docker run -d -p 8000:8000 --name rh-recrutement-container rh-recrutement
    ```

4. **Cloner le dépôt du projet**:
    Ouvrez votre navigateur et accédez à http://localhost:8000.

# Architecture du Projet
```text
/backend
│
├── app/
│   ├── __init__.py
│   ├── main.py                # Point d'entrée de l'application
│   ├── cv_extractor.py        # Module pour extraire les données des CVs
│   ├── models/
│   │   ├── __init__.py
│   │   └── nlp_models.py      # Initialisation des modèles NLP
│   └── utils/
│       ├── __init__.py
│       └── helpers.py         # Fonctions utilitaires
│
├── Dockerfile                 # Fichier pour construire l'image Docker
├── requirements.txt           # Dépendances Python
├── README.md                  # Documentation du projet
└── frontend/
    ├── package.json           # Dépendances NodeJS
    ├── public/
    └── src/                   # Code source du front-end
        ├── App.js
        └── index.js
```

# Technologies Utilisées
## Back-End
 - Python
 - pdfplumber
 - HuggingFace
 - OpenIA - GPT4-o-mini

## Transformers (Hugging Face)
 - spaCy
 - Front-End
 - Vue.js
 - Node.js

**Lancer le Front-End**
Cloner le front :  https://github.com/cleverIACV/frontend.git

