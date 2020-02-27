#!/usr/bin/env python
import pika
import os


def main():
    RABBIT_MQ_ADDR = os.getenv('RABBIT_MQ_ADDR')
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(RABBIT_MQ_ADDR))
    channel = connection.channel()
    print("Hello, World!")


if __name__ == "__main__":
    main()
