import json
import pika   # Python AMQP Library
import os
import datetime
from dotenv import load_dotenv

load_dotenv()
# get Environment Variables
RABBIT_HOST = os.environ['RABBIT_HOST']
RABBIT_USER = os.environ['RABBIT_USER']
RABBIT_PWD = os.environ['RABBIT_PWD']

credentials = pika.PlainCredentials(RABBIT_USER, RABBIT_PWD)
parameters = pika.ConnectionParameters(credentials=credentials, host=RABBIT_HOST, virtual_host=RABBIT_USER)  # CloudAMQP sets the vhost same as User
connection = pika.BlockingConnection(parameters)  # Establishes TCP Connection with RabbitMQ
channel = connection.channel()
channel.exchange_declare(exchange='test', exchange_type='fanout')
channel.basic_publish(exchange='test', routing_key='', body=json.dumps({
    'vietnamese': 'Xin chào thế giới',
    'english': 'Hello World!',
    'china': '你好世界',
    'time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
}).encode('UTF-8'))

print(" [x] Message send")
connection.close()