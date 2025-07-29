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