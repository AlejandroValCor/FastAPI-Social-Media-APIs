import pytest
from jose import jwt
from app import schemas
from app.config import settings

"""
def test_root(client):
    response = client.get("/")

    print(response.json().get('message'))
    assert response.json().get('message') == "Happy Corgi!!! <3 Guau Guau!"
    assert response.status_code == 200
"""

def test_create_user(client):
    response = client.post("/users/", json=
        {
            "email": "corgi@dog.com",
            "password": "HappyCorgi"
        })
    
    new_user = schemas.UserOut(**response.json())

    assert new_user.email == "corgi@dog.com"
    assert response.status_code == 201

def test_login_user(client, test_user):
    response = client.post("/login", data=
        {
            "username": test_user["email"],
            "password": test_user["password"]
        })
    
    login_response = schemas.Token(**response.json())

    payload = jwt.decode(login_response.access_token, settings.secret_key, algorithms=[settings.algorithm])

    id = payload.get("user_id")
    assert id == test_user['id']
    assert login_response.token_type ==  "bearer"
    assert response.status_code == 200

@pytest.mark.parametrize("email, password, status_code", [
    ('wrongemail@wrong.com', 'HappyCorgi', 403),
    ('corgi@dog.com', 'Wrong Password', 403),
    ('wrongemail@wrong.com', 'Wrong Password', 403),
    (None, 'HappyCorgi', 422),
    ('corgi@dog.com', None, 422),
])
def test_incorrect_login(client, test_user, email, password, status_code):    
    data = {}

    if email is not None:
        data["username"] = email
    if password is not None:
        data["password"] = password

    response = client.post('/login/', data=data)

    assert response.status_code == status_code
    # assert response.json().get("detail") == "Invalid credentials."