from pydantic import BaseModel
from typing import List, Optional


class Detection(BaseModel):
    confidence: float
    bbox: List[int]
    action: str
    duration: float
    phase: str
    player_action: bool

class Event(BaseModel):
    timestamp: str
    sample_id: str
    boss: str
    game: str
    source: str
    frame_id: int
    detections: List[Detection]