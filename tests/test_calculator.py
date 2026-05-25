import pytest
from fastapi.testclient import TestClient

from src.app import app, calculate

client = TestClient(app)


@pytest.mark.parametrize(
    ("num1", "num2", "operation", "expected"),
    [
        (10, 5, "add", 15),
        (10, 5, "subtract", 5),
        (10, 5, "multiply", 50),
        (10, 3, "divide", 3),
    ],
)
def test_calculate_valid_operations(num1, num2, operation, expected):
    assert calculate(num1, num2, operation) == expected


def test_calculate_rejects_invalid_operation():
    with pytest.raises(ValueError, match="Unsupported operation"):
        calculate(10, 2, "mod")


def test_calculate_rejects_division_by_zero():
    with pytest.raises(ZeroDivisionError, match="Cannot divide by zero"):
        calculate(10, 0, "divide")


def test_calculate_rejects_non_integer_values():
    with pytest.raises(TypeError, match="num1 must be an integer"):
        calculate(True, 2, "add")


def test_calculator_endpoint_success():
    response = client.get("/calculator", params={"num1": 8, "num2": 4, "operation": "divide"})
    assert response.status_code == 200
    assert response.json()["result"] == 2


def test_calculator_endpoint_invalid_operation():
    response = client.get("/calculator", params={"num1": 8, "num2": 4, "operation": "invalid"})
    assert response.status_code == 400
    assert "Unsupported operation" in response.json()["detail"]


def test_calculator_endpoint_divide_by_zero():
    response = client.get("/calculator", params={"num1": 8, "num2": 0, "operation": "divide"})
    assert response.status_code == 400
    assert response.json()["detail"] == "Cannot divide by zero"


def test_calculator_endpoint_non_integer_input():
    response = client.get("/calculator", params={"num1": "abc", "num2": 4, "operation": "add"})
    assert response.status_code == 422
