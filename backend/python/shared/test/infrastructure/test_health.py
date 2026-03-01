
from fastapi.testclient import TestClient
import pytest
from manage import app


client = TestClient(app)

def test_root():
    response=client.get("/")
    assert response.status_code==200
    assert response.json()=={"Hello":"World"}

@pytest.mark.parametrize(
        "name, age, expected", [
        ("Manas", 25, "Hello Manas, you are 25 years old!"),
        ("Alice", 30, "Hello Alice, you are 30 years old!"),
        ("Bob", 18, "Hello Bob, you are 18 years old!"),
        ("Test", 1, "Hello Test, you are 1 years old!"),
        ]
)
def test_greet(name:str,age:int,expected:str):
    response=client.get("/greet", params={"name":name, "age":age})
    assert response.status_code==200
    assert response.json()