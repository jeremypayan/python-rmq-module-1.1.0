import os
import yaml
from pathlib import Path
from dotmap import DotMap
from dotenv import load_dotenv 
load_dotenv()

def load_only_current_env(config):
	''' Function that takes a config file as input to return the 
	specific config corresonding to the ENV environnement variable (dev, test, preprod, prod) 
	'''
	configs = yaml.load(config,  Loader=yaml.FullLoader)
	print(configs[os.getenv('ENV')])
	return configs[os.getenv('ENV')]


config_files = [os.path.join(r, file) for r, d, f in os.walk(os.environ['CONFIG']) for file in f if '.yaml' in file]
config = DotMap({Path(cfg).stem: load_only_current_env(open(cfg, 'r')) for cfg in config_files})
