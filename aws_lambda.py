import pika   # Python AMQP Library
import boto3
import os
import datetime
from base64 import b64decode

# get Environment Variables
RABBIT_HOST = os.environ['RABBIT_HOST']
RABBIT_USER = os.environ['RABBIT_USER']
RABBIT_PWD_ENCRYPTED = os.environ['RABBIT_PWD']
# Decrypt Password
RABBIT_PWD_DECRYPTED = boto3.client('kms').decrypt(CiphertextBlob=b64decode(RABBIT_PWD_ENCRYPTED))['Plaintext']
credentials = pika.PlainCredentials(RABBIT_USER, RABBIT_PWD_DECRYPTED)
parameters = pika.ConnectionParameters(credentials=credentials, ssl=True, host=RABBIT_HOST, virtual_host=RABBIT_USER)  # CloudAMQP sets the vhost same as User
# parameters and credentials ready to support calls to RabbitMQ

def lambda_handler(event, context):
    connection = pika.BlockingConnection(parameters)  # Establishes TCP Connection with RabbitMQ
    channel = connection.channel()  # Establishes logical channel within Connection
    channel.basic_publish(exchange='', routing_key='Lambda', body='Howdy RabbitMQ, Lambda Here!! ' + datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y") + ' UTC')     # Send Message
    connection.close()        # Close Connection and Channel(s) within