from fastapi import FastAPI
from app.entity.models import Event
from app.repository.event_repository import save_event

app = FastAPI()

@app.post("/process-video")
def process_dummy_video(event: Event):
    print("Received event!!")
    save_event(event)
    return {"status": "Event processed"}


