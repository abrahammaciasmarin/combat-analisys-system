from pydantic import BaseModel
from typing import List, Optional

# {
#   "timestamp": "2025-07-14T13:30:45Z",
# 	"sample_id": "Dragon_King_01",
# 	"boss_in_turn": "Dragon King",
#   "source": "YOLO",
#   "frame_id": 1550,
#   "detections": [
#     {
#       "object": "contour",
#       "confidence": 0.85,
#       "bbox": [100, 50, 150, 100],
#       "action": "movement",
#       "duration": 0.3,
#       "phase": "defense",
#       "game": "Combat Arena",
#       "player_action": false
#     }
#   ]
# }

class Detection(BaseModel):
    object: str
    confidence: float
    bbox: List[int]
    action: str
    duration: float
    phase: str
    game: str
    player_action: bool

class Event(BaseModel):
    timestamp: str
    sample_id: str
    boss_in_turn: str
    source: str
    frame_id: int
    detections: List[Detection]