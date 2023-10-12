import pika
import os 
import sys 
from dotenv import load_dotenv
load_dotenv()
sys.path.append(os.getenv("CONFIG"))
from config import *
import logging
import json


class RabbitMQProducer :
	'''Class that produces messages given a pika channel'''

	def __init__(self, channel, queue_name='', exchange_name='', exchange_type=None, durability=True) : 
		self.exchange_name = exchange_name
		self.exchange_type = exchange_type
		self.queue_name = queue_name
		self.logger = logging.getLogger(self.__class__.__name__)
		self.durability = durability
		self.channel = channel


	def declare_exchange(self, exchange_name, exchange_type) :
		'''Declare a new exchange with a specific type. This exchange will be set as durable if durability=True'''

		try : 
			self.exchange_name = exchange_name
			self.exchange_type = exchange_type
			self.channel.exchange_declare(exchange=self.exchange_name, 
											exchange_type=self.exchange_type, 
											durable=self.durability)
			self.logger.info('an exchange is set')
		except Exception as e : 
			self.logger.warning('exchange has not been declared')


	def declare_queue(self, queue_name='') :
		'''Declare a queue given a queue_name'''
		try : 
			self.queue_name = queue_name
			self.channel.queue_declare(queue=self.queue_name)
			self.logger.info('The queue has been declared')
		except : 
			self.logger.warning('queue has not been declared')



	def publish(self, body) :
		'''Produce messages given exchange and queues in a persistent mode'''
		body_string = json.dumps(body)
		print(self.exchange_name)
		self.channel.basic_publish(exchange=self.exchange_name,
								 routing_key=self.queue_name, 
								 body=body_string, 
								properties=pika.BasicProperties(
                         									delivery_mode = 2, # make message persistent
                         									)	)

	











