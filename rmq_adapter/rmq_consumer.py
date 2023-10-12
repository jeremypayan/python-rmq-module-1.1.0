import pika
import os 
import sys 
from dotenv import load_dotenv
load_dotenv()
sys.path.append(os.getenv("CONFIG"))
from config import *
import logging

class RabbitMQConsumer :
	'''Class that consumes messages given a pika channel'''

	def __init__(self, channel, queue_name='', exchange_name='', exchange_type=None, durability=True, prefetch_count=1) : 
		self.exchange_name = exchange_name
		self.exchange_type = exchange_type
		self.queue_name = queue_name
		self.logger = logging.getLogger(self.__class__.__name__)
		self.durability = durability
		self.channel = channel
		self.prefetch_count = prefetch_count


	def binding_queue(self, queue_name, exchange_name, exchange_type) :
		self.queue_name = queue_name
		self.exchange_name = exchange_name
		self.exchange_type = exchange_type

		self.channel.exchange_declare(exchange=self.exchange_name, exchange_type=self.exchange_type, durable=True)
		print(self.exchange_name)
		print(self.exchange_type)
		result = self.channel.queue_declare(queue=self.queue_name, exclusive=True, durable=True)
		print(result.method.queue)
		self.queue_name = result.method.queue
		self.channel.queue_bind(exchange=self.exchange_name,
                   queue=self.queue_name)



	def consume(self, handler) :

		self.channel.basic_consume(queue=self.queue_name, on_message_callback=handler)
		print(' Waiting for messages. To exit press CTRL+C')
		self.channel.start_consuming()

		
