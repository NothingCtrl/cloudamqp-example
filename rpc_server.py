import pika
import os
import sys
from dotenv import load_dotenv

load_dotenv()

RABBIT_HOST = os.environ['RABBIT_HOST']
RABBIT_USER = os.environ['RABBIT_USER']
RABBIT_PWD = os.environ['RABBIT_PWD']

credentials = pika.PlainCredentials(RABBIT_USER, RABBIT_PWD)
parameters = pika.ConnectionParameters(credentials=credentials, host=RABBIT_HOST, virtual_host=RABBIT_USER)  # CloudAMQP sets the vhost same as User
connection = pika.BlockingConnection(parameters)  # Establishes TCP Connection with RabbitMQ
channel = connection.channel()
channel.queue_declare(queue='rpc_queue')

def fib(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n - 1) + fib(n - 2)

def on_request(ch, method, props, body):
    n = int(body)

    print(" [.] fib(%s)" % n)
    response = fib(n)

    ch.basic_publish(exchange='', routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id=props.correlation_id), body=str(response))
    ch.basic_ack(delivery_tag=method.delivery_tag)

def main():
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='rpc_queue', on_message_callback=on_request)
    print(" [x] Awaiting RPC requests")
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
