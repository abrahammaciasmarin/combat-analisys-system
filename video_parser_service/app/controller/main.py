from fastapi import FastAPI, HTTPException

from app.detectors.opencv_detector import delete_duplicate_files, opencv_load_video
from app.entity.models import Event
from app.repository.event_repository import save_event
from app.config.logger_config import setup_logger
from app.detectors.yolo_detector import yolo_load_video
from app.detectors.prelabel_script import pre_label
from app.detectors.prelabel_script import wukong_prelabel_running
from app.detectors.yolo_detector import  json_to_txt
import logging, torch

setup_logger()
app = FastAPI()
print(torch.__version__)
print(torch.cuda.is_available())

#yolo_load_video()
#pre_label()
opencv_load_video()
#delete_duplicate_files()
#yolo_trainer()
#wukong_prelabel_running()
#json_to_txt()

@app.post("/process-video")
def process_dummy_video(event: Event):
    logging.info("Received event!!")
    try:
        save_event(event)
        return {"status": "Event processed"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



