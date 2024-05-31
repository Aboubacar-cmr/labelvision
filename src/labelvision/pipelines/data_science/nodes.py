from ultralytics import YOLO
import os


def train_yolo(data_yaml: str, img_size: int, epochs: int):
    model = YOLO("yolov5n.pt")
    result = model.train(data=os.path.join(os.getcwd(), data_yaml), epochs=epochs, imgsz=img_size)
    return model
