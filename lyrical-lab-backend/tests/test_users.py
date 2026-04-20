from app import schemas
from app import oauth2 as settings
import pytest


def test_index(client):
    res = client.get("/")
    print(res)
    assert res.json().get("message") == "Hello world!"
    assert res.status_code == 200


def test_create_user(client):
    res = client.post("/api/users/", json={"artist_name": "kaystee", "age": 20, " password": "1234", "email": "kaystee@gmail.com", })

    new_user = schemas.UserOut(**res.json())
    print(new_user)
    # new_user = res.json()
    # assert new_user.email  == "kaystee@gmail.com"
    # assert new_user.artist_name == "kaystee"
    # assert new_user.age == 20
    # assert new_user.blocked == False
    assert res.status_code == 201