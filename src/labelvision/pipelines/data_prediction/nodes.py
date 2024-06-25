"""
This is a boilerplate pipeline 'data_prediction'
generated using Kedro 0.19.6
"""


from ultralytics import YOLO
import os
import torch
import cv2
import tensorflow as tf

def prediction2(image_path: str, model_path: str, path_result: str):
    # Charger le modèle YOLO
    model = YOLO(model_path)

    # Faire des prédictions
    results = model.predict(image_path, save=True, imgsz=320, conf=0.1)

    for r in results:
        print(r.boxes) 









def prediction(image_path: str, model_path: str, path_result: str):
    # Charger le modèle YOLO
    model = YOLO(model_path)
    # Faire des prédictions sur l'image
    results = model.predict(image_path)
    
    # Charger l'image originale pour l'annotation
    image = cv2.imread(image_path)
    
    # Annoter l'image avec les résultats de prédiction
    for result in results:
        for box in result.boxes:
            # Extraire les coordonnées du bounding box
            x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
            # Dessiner le rectangle du bounding box
            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
            # Ajouter le label de la classe et la confiance
            single_tensor_cls = tf.constant(box.cls[0])
            classe = int(float(tf.strings.as_string(single_tensor_cls).numpy().decode("utf-8")))

            single_tensor_conf = tf.constant(box.conf[0])
            conf = tf.strings.as_string(single_tensor_conf).numpy().decode("utf-8")
            
            label = f"{result.names[classe]} {float(conf):.2f}"
            cv2.putText(image, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    
    # Sauvegarder l'image annotée
    cv2.imwrite(path_result, image)
    
    return results