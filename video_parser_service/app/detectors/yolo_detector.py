import logging
from datetime import datetime
from ultralytics import YOLO
from app.entity.models import Detection, Event
from app.repository.event_repository import save_event
from app.events.publisher import publish_new_event
from app.config.config_loader import load_config
import cv2, gc,os, json, yaml,shutil, torch

LOAD_CFG = load_config()

def pre_label():
    # Ejemplo de escritura
    for nombre_archivo in os.listdir("prelabeled_dataset/labels"):
        if nombre_archivo.endswith(".txt"):
            ruta_completa = os.path.join("prelabeled_dataset/labels", nombre_archivo)
            try:
                with open(ruta_completa, 'a') as archivo:  # 'a' para añadir, 'w' para sobreescribir
                    archivo.write("0 0.504232 0.685892 0.098307 0.459559\n")
                print(f"Se escribió en: {nombre_archivo}")
            except Exception as e:
                print(f"Error al escribir en {nombre_archivo}: {e}")
        else:
            ACTION_NAME = "wukong_running.webm"
            VIDEO_PATH = "video/"+ACTION_NAME
            OUTPUT_DIR = "prelabeled_dataset"
            FRAME_INTERVAL = 5  # Extrae cada 5 frames
            MODEL = YOLO("yolov8l.pt")

            # Crear carpetas
            #os.makedirs(f"{OUTPUT_DIR}/images", exist_ok=True)
            #os.makedirs(f"{OUTPUT_DIR}/labels", exist_ok=True)

            # Cargar video
            video = cv2.VideoCapture(VIDEO_PATH)
            frame_id = 0

            while True:
                success, frame = video.read()
                if not success:
                    break

                if frame_id % FRAME_INTERVAL != 0:
                    frame_id += 1
                    continue

                # Guardar imagen
                img_name = f"frame_{frame_id}.jpg"
                img_path = f"{OUTPUT_DIR}/images/{img_name}"
                cv2.imwrite(img_path, frame)

                # Aplicar YOLO
                results = MODEL.predict(frame)[0]
                height, width, _ = frame.shape

                # Guardar etiquetas en formato YOLO
                label_path = f"{OUTPUT_DIR}/labels/{img_name.replace('.jpg','.txt')}"
                with open(label_path, "w") as f:
                    for box in results.boxes:
                        cls_id = int(box.cls[1])
                        obj_cls = results.names[int(box.cls[0])]
                        conf = float(box.conf[0])
                        if conf < 0.5:
                            continue

                        x1, y1 = 873.75, 496.25
                        x2, y2 = 1062.5, 996.25
                        img_w, img_h = 1920, 1088

                        xc = ((x1 + x2) / 2) / img_w  # → ≈ 0.5039
                        yc = ((y1 + y2) / 2) / img_h  # → ≈ 0.6866
                        w = (x2 - x1) / img_w  # → ≈ 0.0985
                        h = (y2 - y1) / img_h  # → ≈ 0.4599

                        f.write(f"{cls_id} {xc:.6f} {yc:.6f} {w:.6f} {h:.6f}\n")

                frame_id += 1



def yolo_load_video():
    device = "cuda" if torch.cuda.is_available() else "cpu"
    logging.info("+++++++++++++++++++++++++"+device+"+++++++++++++++++++++++++++++++++")
    #model_idle = YOLO("C:/Users/abrah/combat-analisys-system/runs/detect/wukong_idle_model/weights/best.pt").to(device)
    model_running = YOLO("C:/Users/abrah/combat-analisys-system/runs/detect/wukong_running_model/weights/best.pt").to(device)
    video_name = "wukong_running_01_02.webm"
    video = cv2.VideoCapture("video/"+video_name)
    data_arr = video_name.split("_")
    game = data_arr[0]
    boss_in_turn = data_arr[1]
    sample_id =data_arr[2]
    boss_phase = data_arr[3]
    frame_id = 0
    total_frames = 1000
    yolo_process_video(video, model_running, frame_id, game, boss_in_turn, sample_id, boss_phase, total_frames)

def yolo_process_video(video, model_running, frame_id, game, boss_in_turn, sample_id, boss_phase, total_frames):
    detections: list[Detection] = []
    while True:
        success, frame = video.read()
        if not success:
            break

        if frame_id % 5 != 0:
            frame_id += 1
            continue

        timestamp = datetime.utcnow().isoformat()
        results_running = model_running.predict(frame, conf=0.9)[0]

        for result in results_running:
            for box in result.boxes:
                xyxy = box.xyxy[0].tolist()
                obj_cls = result.names[int(box.cls[0])]
                confidence = float(box.conf[0])
                if confidence < 0.5:
                    continue

                create_detections(obj_cls, confidence, xyxy, boss_phase, game, detections, "wukong_runing")
        save_event(create_combat_event(timestamp, sample_id, boss_in_turn, frame_id, detections))

        del results_running
        gc.collect()
        frame_id += 1
    boss_actions = []
    for detection in detections:
        boss_actions.append(detection.action)
    publish_new_event(sample_id,boss_in_turn,total_frames,boss_actions)

def create_combat_event(timestamp, sample_id, boss_in_turn, frame_id, detections):
    event = Event(
        timestamp=timestamp,
        sample_id=sample_id,
        boss_in_turn=boss_in_turn,
        source="YOLO",
        frame_id=frame_id,
        detections=detections
    )
    return event
def create_detections(obj_cls, confidence, xyxy, boss_phase, game, detections,action_state):
    detection = Detection(
        object=obj_cls,
        confidence=confidence,
        bbox=[int(xyxy[0]), int(xyxy[1]), int(xyxy[2]), int(xyxy[3])],
        action=action_state,
        duration=0.0,
        phase=boss_phase,
        game=game,
        player_action=False
    )
    detections.append(detection)



def json_to_txt():
    with open("combat.yml", "r") as file:
        combat_cfg = yaml.safe_load(file)
    for filename in os.listdir(combat_cfg["frames"]):
        if not filename.endswith(".json"):
            continue

        json_path = os.path.join(combat_cfg["frames"], filename)
        with open(json_path, "r") as file:
            data = json.load(file)

        img_w, img_h = data["imageWidth"], data["imageHeight"]
        lines = []

        for shape in data["shapes"]:
            if shape["shape_type"] != "rectangle":
                continue

            x1, y1 = shape["points"][0]
            x2, y2 = shape["points"][1]
            label = shape["label"]
            class_id = 0
            if label == "grate_sage":
                class_id = 0
            elif label == "grate_sage_idle":
                class_id = 1
            elif label == "grate_sage_dodge":
                class_id=2
            elif label == "grate_sage_charged_attack_01":
                class_id=3
            elif label == "grate_sage_charged_attack_02":
                class_id=4
            elif label == "grate_sage_charged_attack_03":
                class_id=5
            elif label == "grate_sage_charged_attack_04":
                class_id=6


            x_center = ((x1 + x2) / 2) / img_w
            y_center = ((y1 + y2) / 2) / img_h
            width = abs(x2 - x1) / img_w
            height = abs(y2 - y1) / img_h

            lines.append(f"{class_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}")
        txt_name = filename.replace(".json", ".txt")
        txt_path = os.path.join(combat_cfg["txt"], txt_name)
        with open(txt_path, "w") as f:
            f.write("\n".join(lines))
        move_images(combat_cfg["frames"], combat_cfg["val"])
        os.remove(json_path)


def move_images(origen, destino):
    os.makedirs(destino, exist_ok=True)  # crea la carpeta destino si no existe

    for archivo in os.listdir(origen):
        if archivo.lower().endswith((".jpg", ".png", ".jpeg", ".webp")):
            ruta_origen = os.path.join(origen, archivo)
            ruta_destino = os.path.join(destino, archivo)
            shutil.move(ruta_origen, ruta_destino)
            print(f"✅ Movido: {archivo}")