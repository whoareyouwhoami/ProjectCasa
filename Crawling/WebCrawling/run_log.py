import os
import yaml
import logging
from logging.handlers import RotatingFileHandler
logger = logging.getLogger(__name__)

# Open config file
with open("config/config.yaml", 'r') as yamlfile:
    config = yaml.load(yamlfile, Loader=yaml.FullLoader)

# Create log directory
dir_current = os.path.dirname(os.path.realpath(__file__))
dir_log = os.path.join(dir_current, config['logging']['location'])

if not os.path.isdir(dir_log):
    os.mkdir(dir_log)

# Configure logging
file_handler = RotatingFileHandler(os.path.join(config['logging']['location'], config['logging']['filename']),
                                   mode='w')
file_handler.setFormatter(logging.Formatter(config['logging']['format']))

logger.addHandler(file_handler)
logger.setLevel(config['logging']['level'])