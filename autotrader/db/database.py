from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine

USER = 'brook'
PASSWORD = ''
HOST = 'localhost'
POST = '5432'
DB = 'autotrader_development'

CONNECTION_STRING = f'postgresql://{USER}:{PASSWORD}@{HOST}/{DB}'

engine = create_engine(url=CONNECTION_STRING, echo=True)

Base = declarative_base()