import pika
import uuid
import os
import random
from dotenv import load_dotenv

load_dotenv()

RABBIT_HOST = os.environ['RABBIT_HOST']
RABBIT_USER = os.environ['RABBIT_USER']
RABBIT_PWD = os.environ['RABBIT_PWD']

class FibonacciRpcClient(object):

    def __init__(self):
        credentials = pika.PlainCredentials(RABBIT_USER, RABBIT_PWD)
        parameters = pika.ConnectionParameters(credentials=credentials, host=RABBIT_HOST, virtual_host=RABBIT_USER)  # CloudAMQP sets the vhost same as User
        self.connection = pika.BlockingConnection(parameters)  # Establishes TCP Connection with RabbitMQ
        self.channel = self.connection.channel()
        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(queue=self.callback_queue, on_message_callback=self.on_response, auto_ack=True)

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, n):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(exchange='', routing_key='rpc_queue',
                                   properties=pika.BasicProperties(reply_to=self.callback_queue,
                                                                   correlation_id=self.corr_id,),
                                   body=str(n))
        while self.response is None:
            self.connection.process_data_events()
        return int(self.response)

if __name__ == "__main__":
    fibonacci_rpc = FibonacciRpcClient()
    number = random.randint(0, 40)
    print(f" [x] Requesting fib({number})")
    response = fibonacci_rpc.call(number)
    print(" [.] Got %r" % response)