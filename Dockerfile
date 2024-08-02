# Utiliser une image de base officielle de Python
FROM python:3.11-slim

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier le fichier requirements.txt dans le conteneur
COPY requirements.txt /app/

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copier le script d'installation des modèles spaCy
COPY install_spacy_models.sh /app/

# Rendre le script exécutable
RUN chmod +x /app/install_spacy_models.sh

# Exécuter le script pour installer les modèles spaCy
RUN /app/install_spacy_models.sh

# Copier tout le contenu du projet dans le conteneur
COPY . /app/

# Copier et rendre le script d'entrée exécutable
COPY entrypoint.sh /app/
RUN chmod +x /app/entrypoint.sh

# Exposer le port sur lequel Django s'exécute
EXPOSE 8000

# Utiliser le script d'entrée
ENTRYPOINT ["/app/entrypoint.sh"]

# Définir la commande par défaut pour démarrer l'application Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
