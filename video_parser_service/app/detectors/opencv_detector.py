import cv2, os
from collections import defaultdict

# Cargar video o imagen
def opencv_load_video():
    path = "C:/Users/abrah/combat-analisys-system/video_parser_service/video/"
    for file in os.listdir(path):
        video = cv2.VideoCapture(os.path.join(path,file))
        print("charged video", video)
        frame_id = 0
        while True:
            success, frame = video.read()
            if not success:
                break
            if frame_id % 1 != 0:
                frame_id += 1
                continue
            cv2.imwrite(f"frames/frame_{frame_id}_test_01.jpg", frame)
            frame_id += 1

def delete_duplicate_files():
    path="C:/Users/abrah/combat-analisys-system/video_parser_service/frames"
    # Agrupar archivos por nombre base
    nombres_base = defaultdict(list)
    for archivo in os.listdir(path):
        nombre, ext = os.path.splitext(archivo)
        nombres_base[nombre].append(archivo)

    # Eliminar archivos que tienen nombre único (solo una extensión)
    for nombre, archivos in nombres_base.items():
        if len(archivos) == 1:
            archivo_a_eliminar = os.path.join(path, archivos[0])
            os.remove(archivo_a_eliminar)
            print(f"Eliminado: {archivo_a_eliminar}")
