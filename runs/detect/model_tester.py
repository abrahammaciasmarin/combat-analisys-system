import cv2, torch
from ultralytics import YOLO

device = "cuda" if torch.cuda.is_available() else "cpu"
print("++++++++++++++++++++++++"+device+"+++++++++++++++++++++++++")
model_walking = YOLO("C:/Users/abrah/Downloads/wukong_walk_training-20250721T150703Z-1-001/wukong_walk_training/weights/best.pt").to(device)
model_running = YOLO("C:/Users/abrah/Downloads/wukong_running_training-20250721T150703Z-1-001/wukong_running_training/weights/best.pt").to(device)
video = cv2.VideoCapture("C:/Users/abrah/combat-analisys-system/video_parser_service/video/wukong_ancientape_01_02.webm")



while True:
    success, frame = video.read()
    if not success:
        break

    results_walking = model_walking.predict(frame, conf=0.9)[0]
    results_running = model_running.predict(frame, conf=0.8)[0]

    for box in results_walking.boxes:
        conf = float(box.conf[0])
        if not conf < 0.9:
            xyxy = box.xyxy[0].tolist()
            cv2.rectangle(frame, (int(xyxy[0]), int(xyxy[1])), (int(xyxy[2]), int(xyxy[3])), (255, 0, 0), 2)
            cv2.putText(frame, f"walking {conf:.2f}", (int(xyxy[0]), int(xyxy[1] - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        (255, 0, 0), 2)

    for box in results_running.boxes:
        conf = float(box.conf[0])
        if not conf < 0.9:
            xyxy = box.xyxy[0].tolist()
            cv2.rectangle(frame, (int(xyxy[0]), int(xyxy[1])), (int(xyxy[2]), int(xyxy[3])), (0, 255, 0), 2)
            cv2.putText(frame, f"running {conf:.2f}", (int(xyxy[0]), int(xyxy[1] - 10)), cv2.FONT_HERSHEY_SIMPLEX,
                        0.5,
                        (0, 225, 0), 2)

        # ✅ Mostrar resultado en tiempo real
    cv2.imshow("Modelo: Wukong Walking", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video.release()
cv2.destroyAllWindows()



