import pika 
from rmq_adapter.rmq_connection import *
from rmq_adapter.rmq_producer import *
from rmq_adapter.rmq_consumer import *
from dotenv import load_dotenv
load_dotenv()
from config import *
import logging

def handler(ch, method, properties, body) : 
	payload = json.loads(body.decode('utf-8'))
	print("Received {}".format(payload))
	ch.basic_ack(delivery_tag=method.delivery_tag)


def main () :
	connection = Connection()
	channel = connection.get_channel()	
	consumer = RabbitMQConsumer(channel)
	consumer.binding_queue(queue_name='', exchange_name='trame_dispatcher', exchange_type='fanout')
	consumer.consume(handler)
	connection.close()




if __name__ == '__main__':
	try : 
		main()
	except KeyboardInterrupt : 
		print('interrupted')
		try : 
			sys.exit(0)
		except : 
			os.exit(0)
    