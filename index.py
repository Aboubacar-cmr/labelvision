import os
from flask import Flask, request, jsonify, send_file
from kedro.framework.startup import bootstrap_project
from kedro.framework.session import KedroSession
from pathlib import Path

server = Flask(__name__)

# Définir le chemin du projet Kedro
project_path = Path(__file__).resolve().parent

# Bootstrap the Kedro project
metadata = bootstrap_project(project_path)


# Route par défaut
@server.route("/")
def index():
    return "Bienvenue à l'API de detection d'animaux dans une image"


# Route pour l'entraînement du modèle Yolo
@server.route("/api/train", methods=["GET"])
def train():
    with KedroSession.create(project_path=project_path) as session:
        session.run(pipeline_name="__default__")
    return "Pipeline d'entraînement exécuté avec succès"




# Route pour obtenir des prédictions du modèle
@server.route("/api/predict", methods=["POST"])
def predict():
    # Vérifier si le fichier est dans la requête
    if 'file' not in request.files:
        return "No file part", 400

    file = request.files['file']

    # Si aucun fichier n'a été sélectionné
    if file.filename == '':
        return "No selected file", 400

    # Sauvegarder l'image dans le répertoire data/02_img_test/img.jpg
    image_path = os.path.join("data", "02_img_test", "img.jpg")
    file.save(image_path)

    # Effectuer la prédiction
    with KedroSession.create(project_path=project_path) as context:
        context.run(pipeline_name="pred")

    # Récupérer et retourner l'image prédite dans le répertoire data/02_img_test/result.jpg
    result_image_path = os.path.join("data", "02_img_test", "result.jpg")
    
    if not os.path.exists(result_image_path):
        return "Prediction result not found", 404

    return send_file(result_image_path, mimetype='image/jpeg')


if __name__ == '__main__':
    server.run(host='127.0.0.1', port=5002, debug=True)