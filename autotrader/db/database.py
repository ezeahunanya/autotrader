from os import getenv
from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine


DB_SETTINGS = {
    'db': getenv('DB_NAME', 'autotrader_development'),
    'user': getenv('DB_USERNAME', 'autotrader'),
    'password': getenv('DB_PASSWORD', ''),
    'host': getenv('DB_HOST', 'localhost'),
    'port': getenv('DB_PORT', '5432'),
}

CONNECTION_STRING = f"postgresql://{DB_SETTINGS['user']}:{DB_SETTINGS['password']}@{DB_SETTINGS['host']}/{DB_SETTINGS['db']}"
engine = create_engine(url=CONNECTION_STRING, echo=True)
Base = declarative_base()