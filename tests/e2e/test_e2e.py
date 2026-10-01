import requests


BASE_URL = "http://localhost:8000"


def test_health_e2e():
    response = requests.get(f"{BASE_URL}/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_who_e2e():
    response = requests.get(f"{BASE_URL}/who")

    assert response.status_code == 200
    assert response.text != ""