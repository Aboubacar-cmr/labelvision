# Utiliser une image de base officielle Python 3.10.12
FROM python:3.10-slim

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier le fichier requirements.txt et installer les dépendances
COPY requirements.txt req.txt
RUN pip install --no-cache-dir -r req.txt

# Copier le reste de votre application dans le conteneur
COPY . .

# Exposer le port sur lequel l'application Flask s'exécute
EXPOSE 5002

CMD ["python", "index.py"]
