import logging
from datetime import datetime
from ultralytics import YOLO
from app.entity.models import Detection, Event
from app.repository.event_repository import save_event
from app.events.publisher import publish_new_event
from app.config.config_loader import load_config
import cv2, gc, os, torch

LOAD_CFG = load_config()

def yolo_load_video():
    device = "cuda" if torch.cuda.is_available() else "cpu"
    logging.info("+++++++++++++++++++++++++"+device+"+++++++++++++++++++++++++++++++++")
    #model_idle = YOLO("C:/Users/abrah/combat-analisys-system/runs/detect/wukong_idle_model/weights/best.pt").to(device)
    model_running = YOLO("C:/Users/abrah/combat-analisys-system/runs/detect/wukong_running_model/weights/best.pt").to(device)
    video_path = "C:/Users/abrah/combat-analisys-system/video_parser_service_command/video/"
    frame_id = 0
    total_frames = 0
    yolo_process_video(video_path, model_running, frame_id, total_frames)

def yolo_process_video(video_path, model_running, frame_id, total_frames):
    for v in os.listdir(video_path):
        video = cv2.VideoCapture(os.path.join(video_path, v))
        data_arr = v.split("_")
        game = data_arr[0]
        boss = data_arr[1]
        sample_id = data_arr[2]
        phase = data_arr[3]
        detections: list[Detection] = []
        while True:
            success, frame = video.read()
            if not success:
                break

            if frame_id % 5 != 0:
                frame_id += 1
                total_frames+=1
                continue

            timestamp = datetime.utcnow().isoformat()
            results_running = model_running.predict(frame, conf=0.9)[0]

            for result in results_running:
                for box in result.boxes:
                    xyxy = box.xyxy[0].tolist()
                    action = result.names[int(box.cls[0])]
                    confidence = float(box.conf[0])
                    if confidence < 0.5:
                        continue

                    create_detections(confidence, xyxy, phase, detections, action)
            save_event(create_combat_event(timestamp, sample_id, boss, game,frame_id, detections))

            del results_running
            gc.collect()
            frame_id += 1
            total_frames+=1
        publish_new_event(sample_id,boss,game,total_frames)

def create_combat_event(timestamp, sample_id, boss, game,frame_id, detections):
    event = Event(
        timestamp=timestamp,
        sample_id=sample_id,
        boss=boss,
        game=game,
        source="YOLO",
        frame_id=frame_id,
        detections=detections
    )
    return event

def create_detections(confidence, xyxy, boss_phase, detections,action):
    detection = Detection(
        confidence=confidence,
        bbox=[int(xyxy[0]), int(xyxy[1]), int(xyxy[2]), int(xyxy[3])],
        action=action,
        duration=0.0,
        phase=boss_phase,
        player_action=False
    )
    detections.append(detection)