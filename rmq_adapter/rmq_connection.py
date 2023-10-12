import pika
import os 
import sys 
from dotenv import load_dotenv
load_dotenv()
sys.path.append(os.getenv("CONFIG"))
from config import *
import logging

class Connection() :
    '''Rabbit MQ Connection instance to manage the connection id est creating a channel and closing the connection
    ----------
    Methods : 
        get_channel() : 
            Try to etablish the server connection and open a pika channel
        close() : 
            closes the rmq connections '''
    def __init__(self):
        self.user = config.rmq.user
        self.pwd = os.getenv('RMQ-PWD')
        self.port = config.rmq.port
        self.host = config.rmq.host
        self.logger = logging.getLogger(self.__class__.__name__)
        self.connection = None

    def get_channel(self) :
        try : 
            credentials = pika.PlainCredentials(self.user, self.pwd)
            parameters = pika.ConnectionParameters(host=self.host,
                                           port=self.port,
                                           virtual_host='/',
                                           credentials=credentials)
            self.connection = pika.BlockingConnection(parameters)
            self.logger.info('Connected to Rabbit MQ server {}'.format(self.host))
            channel = self.connection.channel()
        
        except Exception as e : 
            print('The connection has not been etablished.')
            self.logger.warning('RMQ connection failure')
            self.logger.debug('Exception {}'.format(e))
            raise e 


        return channel

    def close(self) :
        self.logger.info('Closing the connection to {}'.format(self.host))
        print('Closing the connection to {}'.format(self.host))
        self.connection.close()
        self.connection = None




