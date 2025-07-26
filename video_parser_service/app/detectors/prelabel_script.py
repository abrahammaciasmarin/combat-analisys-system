import cv2
from ultralytics import YOLO
import os

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


def wukong_prelabel_running():
    # # Configuración del modelo y rutas
    ACTION_NAME = "wukong_running.webm"
    VIDEO_PATH = "video/"+ACTION_NAME
    OUTPUT_DIR = "prelabeled_dataset"
    FRAME_INTERVAL = 5  # Extrae cada 5 frames
    MODEL = YOLO("yolov8l.pt")

    # Crear carpetas
    os.makedirs(f"{OUTPUT_DIR}/images", exist_ok=True)
    os.makedirs(f"{OUTPUT_DIR}/labels", exist_ok=True)

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

        img_name = f"frame_{frame_id}.jpg"
        img_path = f"{OUTPUT_DIR}/images/{img_name}"
        cv2.imwrite(img_path, frame)

        results = MODEL.predict(frame)[0]
        height, width, _ = frame.shape
        label_path = f"{OUTPUT_DIR}/labels/{img_name.replace('.jpg', '.txt')}"

        with open(label_path, "w") as f:
            for box in results.boxes:
                cls_id = int(box.cls[0])
                conf = float(box.conf[0])
                name = results.names[cls_id]
                print(name)

                if conf < 0.3:
                    continue

                # Solo si la clase es la que corresponde a Wukong (ajústala si es "person")
                if name not in ["person", "wukong"]:  # pon el nombre real que YOLO detecta para Wukong
                    continue

                x1, y1, x2, y2 = box.xyxy[0]
                x_center = ((x1 + x2) / 2) / width
                y_center = ((y1 + y2) / 2) / height
                w = abs(x2 - x1) / width
                h = abs(y2 - y1) / height

                # Suponiendo clase 1 para wukong_running
                f.write(f"1 {x_center:.6f} {y_center:.6f} {w:.6f} {h:.6f}\n")

        frame_id += 1
