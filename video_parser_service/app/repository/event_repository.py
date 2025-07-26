from app.config.mongo_config import get_connection
from app.events.publisher import publish_new_event
from app.entity.models import Event
import logging

collection = get_connection()

def save_event(event_data: Event):
    logging.info(f"Saving combat event: {event_data}")
    try:
        event_dict = event_data.dict()
        result = collection.insert_one(event_dict)
    except Exception as e:
        logging.error(f"MongoDb: Error to persists combat event -> {e}")
        raise RuntimeError("An error occurs trying to save combat event!!")
    return result.inserted_id