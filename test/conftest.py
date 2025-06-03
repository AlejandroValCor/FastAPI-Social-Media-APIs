from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.main import app
from app.config import settings
from app.database import get_db
from app.database import Base
from app.oauth2 import create_access_token
from app import models
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

@pytest.fixture()
def test_user(client):
    user_data = {
            "email": "corgi@dog.com",
            "password": "HappyCorgi"
        }
    
    response = client.post("/users/", json=user_data)

    assert response.status_code == 201

    new_user = response.json()
    new_user["password"] = user_data["password"]

    return new_user

@pytest.fixture()
def test_user2(client):
    user_data = {
            "email": "corgi123@dog.com",
            "password": "HappyCorgi"
        }
    
    response = client.post("/users/", json=user_data)

    assert response.status_code == 201

    new_user = response.json()
    new_user["password"] = user_data["password"]

    return new_user

@pytest.fixture()
def token(test_user):
    return create_access_token({"user_id": test_user["id"]})

@pytest.fixture()
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }

    return client

@pytest.fixture()
def test_posts(test_user, test_user2, session):
    posts_data = [
    {
        "title": "first title",
        "content": "first content",
        "owner_id": test_user["id"]
    },
    {
        "title": "seccond title",
        "content": "seccond content",
        "owner_id": test_user["id"]
    },
    {
        "title": "third title",
        "content": "third content",
        "owner_id": test_user["id"]
    },
    {
        "title": "fourth title",
        "content": "fourth content",
        "owner_id": test_user2["id"]
    }]

    def create_post_model(post):
        return models.Post(**post)

    post_map = map(create_post_model, posts_data)
    posts = list(post_map)

    session.add_all(posts)
    session.commit()
    posts = session.query(models.Post).all()

    return posts