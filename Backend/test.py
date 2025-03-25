from fastapi.testclient import TestClient

import sys
sys.path.append("C:/Users/user/practice-project/Backend")
from main import app

client = TestClient(app)

def test_get_vacancies():
    response = client.get("/vacancy/", params={"profession": "менеджер"})
    assert response.status_code == 200
    assert len(response.json()) > 0
    assert "Менеджер" in response.json()[0]['name'] 



def test_get_jobs_invalid_profession():
    response = client.get("/vacancy/", params={"profession": "52"})
    assert "[]" in str(response.json())

def test_get_jobs_special_characters():
    response = client.get("/vacancy/", params={"profession": "Джуниор разработчик"})
    assert response.status_code == 200
    assert len(response.json()) > 0
    assert "Джуниор разработчик" in response.json()[0]['name']