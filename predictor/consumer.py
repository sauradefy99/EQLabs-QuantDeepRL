import pika


class Consumer(object):
    def __init__(self, parameters):
        self.parameters = parameters

    def connect(self):
        return pika.BlockingConnection(parameters=self.parameters)

    def close(self):
        self.connection.close()

    def consume_queue(self, queue_name, ack, receiver):
        print("Trying to open a RabbitMQ consumer on queue", queue_name)
        self.channel.basic_consume(
            queue=queue_name, on_message_callback=receiver, auto_ack=ack)
        self.channel.start_consuming()

    def run(self):
        self.connection = self.connect()
        self.channel = self.connection.channel()
