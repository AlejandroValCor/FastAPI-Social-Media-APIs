from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.main import app
from app.config import settings
from app.database import get_db
from app.database import Base
from alembic import command

# Testing database
# SQLAlchemy_database_url = "postgresql://postgres:password123@localhost:5432/Fast API Social Media - Test" In case there is no problem for hard coding test database.
SQLAlchemy_database_url = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name} - Test"

engine = create_engine(SQLAlchemy_database_url)

testingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture()
def session():
    # Run our code before we run our test
    Base.metadata.drop_all(bind=engine) # Putting it here can help you validate any test tables once the testing finishes.
    Base.metadata.create_all(bind=engine)
    #command.upgrade("head") # This will build out all the tables for you but using alembic.

    db = testingSessionLocal()
    try:
        yield db
    finally:
        db.close()

    # Run our code after our test finishes
    # Base.metadata.drop_all(bind=engine) You can keep this here instead, in case you always want to delete them.
    # command.downgrade("base") # This will make sure to remove or rollback all databases to the base version.

@pytest.fixture()
def client(session):
    # Run our code before we run our test
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db

    yield TestClient(app)
    
    # Run our code after our test finishes