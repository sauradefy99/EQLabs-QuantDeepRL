import pika


class Publisher(object):
    def __init__(self, parameters, queue):
        self.parameters = parameters
        self.queue = queue

    def connect(self):
        return pika.BlockingConnection(parameters=self.parameters)

    def close(self):
        self.connection.close()

    def publish(self, queue_name, ack, receiver):
        self.channel.basic_publish(
            exchange='', routing_key='', body='Hello World!')

    def run(self):
        self.connection = self.connect()
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.queue)
