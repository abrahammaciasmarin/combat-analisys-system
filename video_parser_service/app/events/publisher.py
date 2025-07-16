import json
import pika

from app.config.rabbit_mq_config import get_rabbit_channel

connection, channel = get_rabbit_channel()


#This function publish a new event to pattern-analyzer-service, each time a new combat sample is processed
def publish_new_event(sample_id, boss_name):
    #Message payload
    message = {
        "sample_id": sample_id,
        "boss_in_turn": boss_name,
        "trigger": "new_event"
    }
    print("Sending combat event to pattern-analyzer-service: ",message)
    channel.basic_publish(
        exchange='event.exchange',
        routing_key='event.new',
        body=json.dumps(message),
        properties=pika.BasicProperties(delivery_mode=2)#the message is persistent, and will be stored in disc not in memory, if the RabbitMQ is restarted the message will survive
    )
    print("Message sent!!")