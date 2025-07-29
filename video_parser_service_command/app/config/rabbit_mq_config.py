import pika, logging
from scipy.special import logit

from app.config.config_loader import load_config

config = load_config()
rabbitmq_config = config["messaging"]["rabbitmq"]


def get_rabbit_channel():
    credentials = pika.PlainCredentials(rabbitmq_config["username"], rabbitmq_config["password"])
    params = pika.ConnectionParameters(rabbitmq_config["host"], rabbitmq_config["port"], '/', credentials)
    try:
        connection = pika.BlockingConnection(params)
        channel = connection.channel()

        channel.exchange_declare(exchange=rabbitmq_config["exchange"], exchange_type=rabbitmq_config["exchange_type"])
        channel.queue_declare(queue=rabbitmq_config["queue"], durable=rabbitmq_config["durable"])
        channel.queue_bind(exchange=rabbitmq_config["exchange"], queue=rabbitmq_config["queue"], routing_key=rabbitmq_config["routing_key"])
    except pika.exceptions.AMQPConnectionError as e:
        logging.error(f"RabbitMQ: Connection ERROR -> {e}")
        raise RuntimeError("Connection to RabbitMQ wasn't established")

    return connection, channel