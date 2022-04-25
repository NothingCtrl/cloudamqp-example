import time
import json
import sys
import pika   # Python AMQP Library
import os
import random
from dotenv import load_dotenv

load_dotenv()
# get Environment Variables
RABBIT_HOST = os.environ['RABBIT_HOST']
RABBIT_USER = os.environ['RABBIT_USER']
RABBIT_PWD = os.environ['RABBIT_PWD']

def main():
    credentials = pika.PlainCredentials(RABBIT_USER, RABBIT_PWD)
    parameters = pika.ConnectionParameters(credentials=credentials, host=RABBIT_HOST,
                                           virtual_host=RABBIT_USER)  # CloudAMQP sets the vhost same as User
    connection = pika.BlockingConnection(parameters)  # Establishes TCP Connection with RabbitMQ
    channel = connection.channel()
    channel.exchange_declare(exchange='test', exchange_type='fanout')
    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue
    channel.queue_bind(exchange='test', queue=queue_name)

    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body)
        print(f"     |--> Decode: {json.loads(body.decode('UTF-8'))}")

    # channel.basic_consume(queue=QUEUE_NAME, auto_ack=True, on_message_callback=callback)    # single worker
    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)     # multi worker
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)