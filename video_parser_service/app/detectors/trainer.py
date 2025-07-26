from ultralytics import YOLO
import cv2, gc, torch

torch.cuda.empty_cache()
gc.collect()

model = YOLO("yolov8l.pt")  # Puedes usar yolov8n para empezar más rápido
model.train(
    data="C:/Users/abrah/combat-analisys-system/video_parser_service/combat.yml",
    cache="disk",
    epochs=100,
    imgsz=640,
    device = 0,
    workers=0,
    batch=4,
    name="wukong_walking_model")