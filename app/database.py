from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings


SQLAlchemy_database_url = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

engine = create_engine(SQLAlchemy_database_url)

sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()

# Connect to database with postgres driver, in case you want to use raw SQL instead of SQL alchemy.
"""
import psycopg2
from psycopg2.extras import RealDictCursor
import time

tries = 0

while tries < 5:
    try:
        conn = psycopg2.connect(host='localhost', database='Fast API Social Media', user='postgres', password='password123', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was succesfull!")
        break
    except Exception as error:
        print("Connecting to database failed")
        print("Error: ", error)
        time.sleep(2)
    
    tries += 1
"""