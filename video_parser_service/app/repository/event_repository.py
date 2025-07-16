from app.config.mongo_config import get_connection
from app.events.publisher import publish_new_event
from app.entity.models import Event
collection = get_connection()

def save_event(event_data: Event):
    print("Saving event",event_data)
    event_dict = event_data.dict()
    result = collection.insert_one(event_dict)
    publish_new_event(event_data.sample_id, event_data.boss_in_turn)
    return result.inserted_id