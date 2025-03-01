import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch
from app.main import app
from app.hand.infrastructure.persistance.hand_json_repository import hand_repository

client = TestClient(app)


@pytest.fixture
def mock_hand_repository():
    """Mock the hand_repository to avoid real service calls."""
    with patch.object(hand_repository, "get_all", new_callable=AsyncMock) as mock_repo:
        yield mock_repo


test_user_id = "01a01v02-ed1f-11ef-901b-0ade7a4f7cd3"


def test_get_hands_success():
    """Test retrieving a hand successfully (200 OK)."""
    # existing_hand_id = "785dd6d5-5391-498e-abbf-b9018fdfc0f3"

    response = client.get(
        "/api/v1/hands",
        cookies={"user_id": test_user_id},
    )

    assert response.status_code == 200
    json_data = response.json()
    assert isinstance(json_data, list)


def test_get_hands_missing_user_id():
    """Test error when user_id is missing in cookies (401 Unauthorized)."""
    response = client.get("/api/v1/hands")  # No cookies

    assert response.status_code == 401
    assert response.json()["detail"] == "Missing user_id in cookies"


def test_get_hands_internal_server_error(mock_hand_repository):
    """Test handling of unexpected server error (500 Internal Server Error)."""
    mock_hand_repository.side_effect = Exception(
        "Unexpected DB error"
    )  # Simulate error

    response = client.get("/api/v1/hands", cookies={"user_id": "valid_user"})

    assert response.status_code == 500
    assert "Error retrieving hands" in response.json()["detail"]
