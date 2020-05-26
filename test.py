import pytest
import json
import sys

sys.path.append(".")
from api import app

@pytest.fixture
def client():
    client = app.test_client()

    return client

def test_crawling_POST1(client):
    login_info = {
        "productID" : "530671371510",
        "userID" : "jelly7614",
        "userPasswd" : "1029386a!"
    }
    resp = client.post(
        "/userLogin",
        data=json.dumps(login_info),
        content_type="application/json"
    )
    assert resp.status_code == 200

def test_crawling_POST2(client):
    login_info = {
        "productID" : "613152621346",
        "userID" : "jelly7614",
        "userPasswd" : "1029386a!"
    }
    resp = client.post(
        "/userLogin",
        data=json.dumps(login_info),
        content_type="application/json"
    )
    assert resp.status_code == 200

def test_crawling_POST3(client):
    login_info = {
        "productID" : "601212179618",
        "userID" : "jelly7614",
        "userPasswd" : "1029386a!"
    }
    resp = client.post(
        "/userLogin",
        data=json.dumps(login_info),
        content_type="application/json"
    )
    assert resp.status_code == 200