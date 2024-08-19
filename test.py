from fastapi.testclient import TestClient as FastTestClient
from flask.testing import FlaskClient as FlaskTestClient
from bs4 import BeautifulSoup
from fastapi import app as fastapi_app
from flask import app as flask_app

fastapi_client = FastTestClient(fastapi_app)

flask_app.testing = True
flask_client = flask_app.test_client()
flask_client = FlaskTestClient(flask_app)

# FastApi tests

def test_root():
    response = fastapi_client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello FastAPI!"}

def test_add():
    response = fastapi_client.get("/add/5/3")
    assert response.status_code == 200
    assert response.json() == {"total": 8}

    response = fastapi_client.get("/add/-2/-3")
    assert response.status_code == 200
    assert response.json() == {"total": -5}

    response = fastapi_client.get("/add/0/0")
    assert response.status_code == 200
    assert response.json() == {"total": 0}

# Flask test

def test_flask_fruit():
    response = flask_client.get("/fruit")
    assert response.status_code == 200
    soup = BeautifulSoup(response.data, 'html.parser')
    title = soup.find('title').text
    assert title == "Random Fruit"
    fruit_element = soup.find(id="fruit-name")
    assert fruit_element is not None
    assert fruit_element.text in ["apple", "cherry", "orange", "banana", "grape"]
