import pika

def get_rabbit_channel():
    credentials = pika.PlainCredentials('guest', 'guest')
    params = pika.ConnectionParameters('localhost', 5672, '/', credentials)
    try:
        connection = pika.BlockingConnection(params)
        channel = connection.channel()

        channel.exchange_declare(exchange="event.exchange", exchange_type="direct")
        channel.queue_declare(queue="event.queue", durable=True)
        channel.queue_bind(exchange="event.exchange", queue="event.queue", routing_key="event.new")
    except pika.exceptions.AMQPConnectionError as e:(
        print("Connection to RabbitMQ wasn't established: ", e))

    return connection, channel