import pytest
from rmq_adapter.rmq_connection import Connection
import sys
import os
from unittest.mock import Mock
from tests.__mocks__ import pika
from dotenv import load_dotenv
load_dotenv()

sys.path.append(os.getenv("CONFIG"))
from config import *

@pytest.mark.unit
class TestConnection: 
	'''Class to test the Connection class into rmq_connection.py
	---------
	Attributes : 
		connection : Connection object from rmq_adapter.rmq_connection 
	'''
	connection = Connection()  # Test on localhost => suppose that there is a localhost instance 

	## Testing __init__ of Connection class 
	def test_get_user(self) :
		assert self.connection.user == config.rmq.user 

	def test_get_pwd(self) :
		assert self.connection.pwd == os.getenv("RMQ-PWD")

	def test_get_host(self) :
		assert self.connection.host == config.rmq.host 
	
	def test_get_port(self) :
		assert self.connection.port == config.rmq.port

	def test_set_user(self) :
		self.connection.user = 'test'
		assert self.connection.user == 'test'

	def test_set_pwd(self) : 
		self.connection.pwd = 'test'
		assert self.connection.pwd == 'test'

	def test_set_host(self) : 
		self.connection.host = 'test'
		assert self.connection.host == 'test'

	def test_set_port(self) : 
		self.connection.port = 3
		assert self.connection.port == 3

	## To do : test the get_channel() method



'''def _raise_if_not_open(self):
        """If channel is not in the OPEN state, raises ChannelWrongStateError
        with `reply_code` and `reply_text` corresponding to current state.

        :raises exceptions.ChannelWrongStateError: if channel is not in OPEN
            state.
        """
        if self._state == self.OPEN:
            return

        if self._state == self.OPENING:
            raise exceptions.ChannelWrongStateError('Channel is opening, but is not usable yet.')

        if self._state == self.CLOSING:
            raise exceptions.ChannelWrongStateError('Channel is closing.')

        # Assumed self.CLOSED
        assert self._state == self.CLOSED
>       raise exceptions.ChannelWrongStateError('Channel is closed.')'''