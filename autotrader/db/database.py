import os
import sys
import logging

from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine

PROJ_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path = [PROJ_DIR] + sys.path


logger = logging.getLogger('sqlalchemy.engine.Engine')
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(name)s:%(message)s')

file_handler = logging.FileHandler(PROJ_DIR+'/autotrader/logs/database.log')
file_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger.addHandler(file_handler)
# logger.addHandler(stream_handler) # Disabling logging sqlalchemy logs to the console for now.


DB_SETTINGS = {
    'db': os.getenv('DB_NAME', 'autotrader_development'),
    'user': os.getenv('DB_USERNAME', 'autotrader'),
    'password': os.getenv('DB_PASSWORD', ''),
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': os.getenv('DB_PORT', '5432'),
}

CONNECTION_STRING = f"postgresql://{DB_SETTINGS['user']}:{DB_SETTINGS['password']}@{DB_SETTINGS['host']}/{DB_SETTINGS['db']}"
engine = create_engine(url=CONNECTION_STRING)
Base = declarative_base()