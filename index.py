import os
from flask import Flask, request, render_template, send_file, redirect, url_for, jsonify
from kedro.framework.startup import bootstrap_project
from kedro.framework.session import KedroSession
from pathlib import Path
from PIL import Image, ImageStat
from forms import UploadForm

server = Flask(__name__)
server.config['SECRET_KEY'] = 'votre_cle_secrete'  # Remplacez par une clé secrète pour les formulaires

# Définir le chemin du projet Kedro
project_path = Path(__file__).resolve().parent

# Bootstrap the Kedro project
metadata = bootstrap_project(project_path)


# Route par défaut
@server.route("/", methods=["GET", "POST"])
def index():
    form = UploadForm()
    error = None
    if form.validate_on_submit():
        file = form.file.data
        try:
            # Charger et vérifier l'image
            image = Image.open(file)
            image.verify()  # Vérification initiale
            print("Image vérifiée avec succès")
            
            # Réouvrir l'image pour la manipulation
            file.seek(0)
            image = Image.open(file)
            print(f"Taille de l'image reçue : {image.size}")
            
            # Vérifier la taille de l'image
            if image.size != (640, 640):
                raise ValueError(f"La taille de l'image doit être 640x640, mais elle est {image.size}")

            # Vérifier si l'image est vide (tous les pixels ont la même couleur)
            extrema = ImageStat.Stat(image).extrema
            if all(x[0] == x[1] for x in extrema):
                raise ValueError("L'image est vide")
            
            # Sauvegarder l'image dans le répertoire data/02_img_test/img.jpg
            image_path = os.path.join("data", "02_img_test", "img.jpg")
            os.makedirs(os.path.dirname(image_path), exist_ok=True)
            image.save(image_path)
            print(f"Image sauvegardée à {image_path}")
            
            return redirect(url_for('predict'))
        except Exception as e:
            error = str(e)
            print(f"Erreur : {error}")
    return render_template('index.html', form=form, error=error)

# Route pour l'entraînement du modèle Yolo
@server.route("/api/train", methods=["GET"])
def train():
    error = None
    try:
        with KedroSession.create(project_path=project_path) as session:
            session.run(pipeline_name="__default__")
        print("Pipeline d'entraînement exécutée avec succès")
    except Exception as e:
        error = f"Échec de l'exécution de la pipeline d'entraînement : {e}"
        print(f"Erreur : {error}")
    return render_template('train.html', error=error)

# Route pour obtenir des prédictions du modèle
@server.route("/api/predict", methods=["POST"])  # Assurez-vous que cette ligne est correcte
def predict():
    print("Requête reçue")
    
    # Vérifier si le fichier est dans la requête
    if 'file' not in request.files:
        print("Erreur : Pas de fichier dans la requête")
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']

    # Si aucun fichier n'a été sélectionné
    if file.filename == '':
        print("Erreur : Aucun fichier sélectionné")
        return jsonify({"error": "No selected file"}), 400

    try:
        # Charger et vérifier l'image
        image = Image.open(file)
        image.verify()  # Vérification initiale
        print("Image vérifiée avec succès")
        
        # Réouvrir l'image pour la manipulation
        file.seek(0)
        image = Image.open(file)
        print(f"Taille de l'image reçue : {image.size}")
    except Exception as e:
        print(f"Erreur : Fichier image invalide - {e}")
        return jsonify({"error": "Invalid image file"}), 400

    # Vérifier la taille de l'image
    if image.size != (640, 640):
        print(f"Erreur : Taille de l'image incorrecte - {image.size}")
        return jsonify({"error": f"Image size must be 640x640, but got {image.size}"}), 400

    # Vérifier si l'image est vide (tous les pixels ont la même couleur)
    extrema = ImageStat.Stat(image).extrema
    if all(x[0] == x[1] for x in extrema):
        print("Erreur : Image vide")
        return jsonify({"error": "Image is empty"}), 400
    else:
        print(f"Extrêmes de l'image : {extrema}")

    # Sauvegarder l'image dans le répertoire data/02_img_test/img.jpg
    image_path = os.path.join("data", "02_img_test", "img.jpg")
    try:
        os.makedirs(os.path.dirname(image_path), exist_ok=True)
        image.save(image_path)
        print(f"Image saved to {image_path}")
    except Exception as e:
        print(f"Erreur : Échec de la sauvegarde de l'image - {e}")
        return jsonify({"error": f"Failed to save image: {e}"}), 500

    # Effectuer la prédiction
    try:
        with KedroSession.create(project_path=project_path) as context:
            context.run(pipeline_name="pred")
        print("Pipeline de prédiction exécutée avec succès")
    except Exception as e:
        print(f"Erreur : Échec de l'exécution de la pipeline de prédiction - {e}")
        return jsonify({"error": f"Failed to run prediction pipeline: {e}"}), 500

    # Récupérer et retourner l'image prédite dans le répertoire data/02_img_test/result.jpg
    result_image_path = os.path.join("data", "02_img_test", "result.jpg")
    
    if not os.path.exists(result_image_path):
        print("Erreur : Résultat de la prédiction non trouvé")
        return jsonify({"error": "Prediction result not found"}), 404

    # Envoyer l'image prédite avec un message de succès
    return send_file(result_image_path, mimetype='image/jpeg')


# Route pour évaluer le modèle
@server.route("/api/evaluate", methods=["GET"])
def evaluate():
    error = None
    metrics = None
    try:
        with KedroSession.create(project_path=project_path) as context:
            context.run(pipeline_name="eval")
        print("Pipeline d'évaluation exécutée avec succès")
        
        # Lire les métriques depuis le fichier généré par la pipeline
        metrics_path = os.path.join("runs", "detect", "train18", "metrics.txt")
        if os.path.exists(metrics_path):
            with open(metrics_path, 'r') as file:
                metrics = file.read()
        else:
            error = "Fichier de métriques non trouvé"
            print(f"Erreur : {error}")

    except Exception as e:
        error = f"Échec de l'exécution de la pipeline d'évaluation : {e}"
        print(f"Erreur : {error}")

    return render_template('evaluation.html', metrics=metrics, error=error)


# Route pour afficher l'image de résultat
@server.route('/data/02_img_test/result.jpg')
def result_file():
    result_image_path = os.path.join("data", "02_img_test", "result.jpg")
    return send_file(result_image_path, mimetype='image/jpeg')


if __name__ == '__main__':
    server.run(host='127.0.0.1', port=5000, debug=True)
