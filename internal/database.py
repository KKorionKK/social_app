from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

conn_string = 'postgresql+psycopg2://postgres:123gr@localhost:4321/social_app'

engine = create_engine(conn_string)

SessionLocal = sessionmaker(autoflush=False, bind=engine)

Base = declarative_base()
