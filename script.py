import requests
from io import BytesIO
from PIL import Image
import argparse
import os

# Configurer les arguments de ligne de commande
parser = argparse.ArgumentParser(description='Tester l\'API de prédiction avec une image.')
parser.add_argument('image_path', type=str, help='Le chemin vers l\'image à utiliser pour le test.')
args = parser.parse_args()

url = "http://127.0.0.1:5000/api/predict"  # Assurez-vous que l'URL est correcte

# Ouvrir et rogner l'image
image_path = args.image_path
if not os.path.exists(image_path):
    print(f"Erreur: Le fichier {image_path} n'existe pas.")
    exit(1)

try:
    image1 = Image.open(image_path)
except Exception as e:
    print(f"Erreur: Impossible d'ouvrir l'image - {e}")
    exit(1)

image_rognee = image1.crop((20, 30, 50, 236))
image_vide = Image.new("RGB", (10, 10))  # Créer une image vide
images = [image1, image_rognee, image_vide]

for idx, image in enumerate(images):
    try:
        # Convertir l'image en octets
        image_bytes = BytesIO()
        image.save(image_bytes, format="JPEG")
        image_bytes.seek(0)
        files = {'file': ('image.jpg', image_bytes, 'image/jpeg')}
        response = requests.post(url, files=files)
        print(f"Test Image {idx + 1}")

        # Afficher le type de contenu de la réponse
        print("Content-Type:", response.headers['Content-Type'])
        
        if 'image/jpeg' in response.headers['Content-Type']:
            # Sauvegarder l'image de la réponse
            result_image_path = f"result_image_{idx + 1}.jpg"
            with open(result_image_path, 'wb') as f:
                f.write(response.content)
            print(f"Image prédite sauvegardée sous {result_image_path}")
            
            # Ouvrir l'image prédite
            predicted_image = Image.open(result_image_path)
            predicted_image.show()
        else:
            # Afficher la réponse JSON
            print("Réponse brute:", response.text)
            print("Réponse JSON:", response.json())
        
        print("=" * 50)
    except Exception as e:
        print("Erreur:", e)
