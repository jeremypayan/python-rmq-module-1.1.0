# Python RabbitMQ module
This repository was created to build a RabbitMQ module with python. The module's objective is to make it faster and easier to :
- connect to RabbitMQ;
- send messages;
- receive messages. 
> The module is based on pika 1.1.0. 

# Module objectives 

## Code aim
The code is made to establish a channel whith the RMQ server through Connection class. Thanks to this channel, we can manipulate a RabbitMQProducer and RabbitMQConsumer objects.
- Connection : Return an object which is able to connect to the RMQ server 
- Producer : Send messages to a given queue according exchange and queue setup 
- Consumer : Listen to a given queue and running a callback function 

## Implementation
The three main classes are : 
- Connection: allow us to connect with a RabbitMQ server. We 'll create channel to operate on the connection object. 
- RabbitMQProducer: with a created channel you can start listening to new messages in a specific queue.
- RabbitMQConsumer: you can send messages to a specific queue and exchange.


# Code architecture 
```
-python-rmq-module-1.1.0
	- README.md
	- LICENCE
	- pytest.ini
	- requirements.txt
	- Makefile
	- rmq_adapter
		- __init__.py 
		- rmq_consumer.py
		- rmq_connection.py
		- rmq_producer.py 
	- tests
		- __init__.py
		- test_connection.py 
		- test_producer.py 
		- test_consumer.py 
		- test_integrations.py 
	- config 
		- config.py 
		- rmq.yaml
```



# Getting Started

1. Make your own fresh virtualenv (if you work on your computer) and activate it
- With conda
	```
	conda create --name <venv-rmq>
	conda activate <venv-rmq> 
	```

2. Git clone the project 


- HTTPS: ```git clone https://enovee.visualstudio.com/cityscoot_Python/_git/python-rmq-module-1.1.0 ```
- SSH: ```git clone enovee@vs-ssh.visualstudio.com:v3/enovee/cityscoot_Python/python-rmq-module-1.1.0```

3. Install the requirements
```
cd python-rmq-module-1.1.0/
conda install pip 
python3 -m pip install -r requirements.txt
```

4. Add the module to your PYTHONPATH
```
export PYTHONPATH='<path-to-your-repo>/python-rmq-module-1.1.0'
```
5. Modify the rmq.yaml with your config 
If you need to modify a config, you can do it directly onto the file ! 

6. create a .env file and set CONFIG, ENV and PWD variables : 
- CONFIG corresponds to the track to config directory on your setup
- ENV corresponds to the corresponding env into rmq.yaml (for now there is only preprod)
- PWD corresponds to your password to access to the RMQ server. It will not be necessary for RMQ local installations. 


6. Make tests and go on ! 
```
make test
```

7. Make your awesome consumers or producers. 
I've added example with ```my_awesome_consumer.py``` and ```my_awesome_producer.py``` files. 

Far example, for the ```producer```, you need to import the package rmq_adapter, create your connection, get the channel and then you can manipulate your producer object and send messages in two line:

```
from rmq_adapter.rmq_producer import *
...

# Make the connection and create a channel
connection = Connection()
channel = connection.get_channel()

# Produce some data
producer = RabbitMQProducer(channel)
producer.declare_exchange(exchange_name=<EXCHANGE>, exchange_type=<EXCHANGE-TYPE>)
#producer.declare_queue('')
producer.publish('some data')

# Close the connection
connection.close()
```


# Configuration 

## environnement variables 
They are in the .env file. The ENV variable corresponds to the env into which you work (for example : test, preprod, prod). 

## Config directory
The rmq.yaml explicits the cofiguration for a given ENV. 
```
preprod :
 host : 'win-preprod-aws.cityscoot.ovh'
 user : 'ep-monitoring-python'
 port : 5672
```
## Matching the good env 
the config.py file gets the config according the rmq.yaml file and the corresponding ENV (preprod for example). 


# Tests
All tests are into the tests directory. They are runned thanks to [Pytest](https://docs.pytest.org/en/stable/). The tests are marked as unit tests or integration test with pytest.ini file. We need the pytest-env library to get environnement variables. 
```
[pytest]
markers =
  integration
  unit
env =
  ENV=preprod
  CONFIG={PWD}/config/
```
To run tests : 
```
make test # run all test functions or classes into the tests directory
make unit-test # Only run unit tests
make integration-test # Only run integration tests
```

## Unit tests 
They test classes into specific files :
- test_connection.py contains all tests corresponding to Connection class. 
- test_consumer.py contains all tests corresponding to RabbitMQConsumer class. 
- test_producer.py contains all tests corresponding to RabbitMQProducer class. 

## Integration tests
They test the 3 main features of our module into the test_integrations.py file :
1. Connection to a RMQ server so that I am able to send messages or listen a queue. 
2. Consume a given queue (listen and run a specific function). 
3. Produce messages to a given queue. 

For example, the TestConnection try to create a connection and test if we are able to send a simple message and consume it. 

```
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
```


