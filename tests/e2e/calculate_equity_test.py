from fastapi.testclient import TestClient
from app.main import app 
import math

client = TestClient(app)

def truncate_to_2_decimals(value):
    return math.floor(value * 100) / 100

def test_calculate_ok():
    body = {
    "hand": ["Qs", "Kh"],
    "range": ["JJ", "AQs", "AQo", "KQs"]
    }
    expected_response = {
    "hand_equity": 0.28,
    "range_equity": 0.62,
    "tie_equity": 0.09
    }

    response = client.post("/api/v1/calculate/equity", json=body)
    json_response = response.json()

    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"
    assert truncate_to_2_decimals(json_response["hand_equity"]) == expected_response["hand_equity"], "Response invalid hand equity"
    assert truncate_to_2_decimals(json_response["range_equity"]) == expected_response["range_equity"], "Response invalid range equity"
    assert truncate_to_2_decimals(json_response["tie_equity"]) == expected_response["tie_equity"], "Response invalid tie equity"

