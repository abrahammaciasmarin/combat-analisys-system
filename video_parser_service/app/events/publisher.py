import json, pika, logging
from app.config.rabbit_mq_config import get_rabbit_channel
from app.config.config_loader import load_config

connection, channel = get_rabbit_channel()
config = load_config()
rabbitmq_config = config["messaging"]["rabbitmq"]

#This function publish a new event to pattern-analyzer-service, each time a new combat sample is processed
def publish_new_event(sample_id, boss_in_turn, total_frames, movements):
    #Message payload
    try:
        message = {
            "sample_id": sample_id,
            "boss_in_turn": boss_in_turn,
            "phase_map": movements,
            "total_frames": total_frames
        }
        logging.info(f"Sending combat event to pattern-analyzer-service: {message}")
        channel.basic_publish(
            exchange=rabbitmq_config["exchange"],
            routing_key=rabbitmq_config["routing_key"],
            body=json.dumps(message),
            properties=pika.BasicProperties(delivery_mode=rabbitmq_config["delivery_mode"])#the message is persistent, and will be stored in disc not in memory, if the RabbitMQ is restarted the message will survive
        )
        logging.info("Message sent!!")
    except Exception as e:
        logging.error(f"RabbitMQ: connection ERROR -> {e}")
        raise RuntimeError("Connection with RabbitMQ failed!!")
