import pytest
from rmq_adapter.rmq_connection import Connection
import sys
import os
import time

sys.path.append(os.environ['CONFIG'])
from config import *

### Connection to RMQ 

def setup_listener(channel, on_message_callback, queue='test', durable=False):
	''' Function that adds a listener inside a created channel'''
	channel.queue_declare(queue=queue, durable=durable)
	channel.basic_consume(queue=queue, on_message_callback=on_message_callback)

	return channel

def wait_for_result(anchor, tries=0,retry_after=.5):
	''' Retries after 500ms if the listener has been called. As we are using an external 
		service that takes time to reply we need to check at different times if our handler has been called '''
	if len(anchor) > 0 or tries > 5: assert len(anchor) > 0
	else:
	    sleep(retry_after)
	    return wait_for_result(anchor, tries + 1)

@pytest.mark.integration
class TestConnection :

	'''Class to test the connection to the RMQ server corresponding to your config (rmq.yaml) and ENV state
	'''

	conn = Connection()
	channel = conn.get_channel()
	queue = 'test'
	body = 'Hello'

	
	def test_rabbitmq_connection(self):
	    # Should be able to create a RabbitMQ connection
	    calls = []
	    def mocked_handler(ch, method, props, body):
	        calls.append(1)
	        ch.close()
	    
	    self.channel = setup_listener(self.channel, mocked_handler)
	    self.channel.basic_publish(
	        exchange='',
	        routing_key=self.queue,
	        body=self.body
	    )

	    self.channel.start_consuming()
	    wait_for_result(calls)

	def teardown_function(self):
		self.channel.queue_delete(queue=self.queue)
   






def test_consume_queue() :
	'''
	Function that checks that we are able to consume a given queue
	 (listen and run a specific function)'''

	assert True


def test_produce() : 
	'''
	functions that checks we are able to publish messages to a queue''' 

	assert True

