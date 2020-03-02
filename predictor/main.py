# -*- coding: utf-8 -*-
import consumer
import publisher
import os
import pika
import threading


def receive_orders(fgsag, asd, fhdug, content):
    print(content)


def open_consumer(queue, ack, receiver):
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


def open_publisher(queue, ack, receiver):
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


def main():
    open_consumer("kraken", False, receive_orders)
    open_consumer("binance", False, receive_orders)


if __name__ == '__main__':
    main()
