from fastapi import FastAPI, HTTPException, Depends
from app.config.logger_config import setup_logger
from app.detectors.yolo_detector import yolo_load_video
import logging, torch

setup_logger()
app = FastAPI()
print(torch.__version__)
print(torch.cuda.is_available())



@app.post("/process-video")
def process_dummy_video():
    logging.info("Processing the video!!")
    try:
        yolo_load_video()
        return {"status": "Video processed"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



