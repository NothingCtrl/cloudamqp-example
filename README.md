# RabbitMQ with CloudAMQP

* Example code using RabbitMQ on [CloudAMQP](https://cloudamqp.com)
* Branch `topic`: Send message to worker based on criteria

### File `.env` example

```env
RABBIT_HOST = host-address
RABBIT_USER = foo
RABBIT_PWD = bar
```

### Notes

Python version 3.6

* `sender.py` send message
* `receiver.py` receive message, single client (worker) mode, auto ack (ref: (1))
* `worker.py` receive message, manual ack mode (ref: (2))
* `aws_lambda.py` for AWS lambda

#### Reference

* (1) https://www.rabbitmq.com/tutorials/tutorial-one-python.html
* (2) https://www.rabbitmq.com/tutorials/tutorial-two-python.html
* (3) https://www.rabbitmq.com/tutorials/tutorial-three-python.html
* (4) https://www.rabbitmq.com/tutorials/tutorial-four-python.html
* (5) https://www.rabbitmq.com/tutorials/tutorial-five-python.html
* (6) https://www.rabbitmq.com/tutorials/tutorial-six-python.html
* (7) https://medium.com/learningsam/publish-to-rabbitmq-from-aws-lambda-cdb66f9f35c5