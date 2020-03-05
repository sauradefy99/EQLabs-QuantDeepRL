# -*- coding: utf-8 -*-
import consumer
import publisher
import os
import pika
import threading


def receive_orders(fgsag, asd, fhdug, content):
    print(content)


class Predictor(object):
    def receive_orders(self, fgsag, asd, fhdug, content):
        print(content)

    def open_consumer(self, queue, ack, receiver):
        RABBIT_MQ_HOST = os.getenv('RABBIT_MQ_HOST')
        RABBIT_MQ_PORT = os.getenv('RABBIT_MQ_PORT')
        if not RABBIT_MQ_HOST or not RABBIT_MQ_PORT:
            RABBIT_MQ_HOST = u'localhost'
            RABBIT_MQ_PORT = 5672
        c = consumer.Consumer(pika.ConnectionParameters(RABBIT_MQ_HOST,
                                                        RABBIT_MQ_PORT,
                                                        '/'))
        c.run()
        thread = threading.Thread(target=c.consume_queue, args=(
            queue, ack, receiver))
        thread.start()

    def open_publisher(self, queue, ack, receiver):
        RABBIT_MQ_HOST = os.getenv('RABBIT_MQ_HOST')
        RABBIT_MQ_PORT = os.getenv('RABBIT_MQ_PORT')
        if not RABBIT_MQ_HOST or not RABBIT_MQ_PORT:
            RABBIT_MQ_HOST = u'localhost'
            RABBIT_MQ_PORT = 5672
        self.p = publisher.Publisher(pika.ConnectionParameters(RABBIT_MQ_HOST,
                                                               RABBIT_MQ_PORT,
                                                               '/'))
        p.run()
        thread = threading.Thread(target=p.consume_queue, args=(
            queue, ack, receiver))
        thread.start()

    def run(self):
        self.open_consumer("kraken", False, receive_orders)
        self.open_consumer("binance", False, receive_orders)
        self.open_publisher()


def main():
    predictor = Predictor()
    predictor.run()


if __name__ == '__main__':
    main()
