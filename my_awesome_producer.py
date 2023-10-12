import pika 
from rmq_adapter.rmq_connection import *
from rmq_adapter.rmq_producer import *
from rmq_adapter.rmq_consumer import *
from dotenv import load_dotenv
load_dotenv()
from config import *
import logging


if __name__ == '__main__':
    connection = Connection()
    channel = connection.get_channel()
    producer = RabbitMQProducer(channel)

    producer.declare_exchange(exchange_name='trame_dispatcher', exchange_type='fanout')
    print(producer.exchange_name)
    #producer.declare_queue('')
    producer.publish('True test')

    connection.close()