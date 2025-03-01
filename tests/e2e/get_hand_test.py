import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch
from app.main import app
from app.hand.infrastructure.persistance.hand_json_repository import hand_repository

client = TestClient(app)


@pytest.fixture
def mock_hand_repository():
    """Mock the hand_repository to avoid real service calls."""
    with patch.object(
        hand_repository, "get_with_neighbors", new_callable=AsyncMock
    ) as mock_repo:
        yield mock_repo


test_user_id = "01a01v02-ed1f-11ef-901b-0ade7a4f7cd3"

# TODO: commented while the environment ets configured
# def test_get_hand_success():
#     """Test retrieving a hand successfully (200 OK)."""
#     existing_hand_id = "785dd6d5-5391-498e-abbf-b9018fdfc0f3"

#     response = client.get(
#         "/api/v1/hands/785dd6d5-5391-498e-abbf-b9018fdfc0f3",
#         cookies={"user_id": test_user_id},
#     )

#     assert response.status_code == 200
#     json_data = response.json()
#     assert json_data["hand"]["id"] == existing_hand_id
#     assert json_data["prev_hand_id"] is None
#     assert json_data["next_hand_id"] is None


def test_get_hand_missing_user_id():
    """Test error when user_id is missing in cookies (401 Unauthorized)."""
    response = client.get("/api/v1/hands/hand123")  # No cookies

    assert response.status_code == 401
    assert response.json()["detail"] == "Missing user_id in cookies"


def test_get_hand_not_found():
    """Test handling when the requested hand is not found (404 Not Found)."""

    response = client.get(
        "/api/v1/hands/hand_not_found", cookies={"user_id": test_user_id}
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Hand not found"


def test_get_hand_internal_server_error(mock_hand_repository):
    """Test handling of unexpected server error (500 Internal Server Error)."""
    mock_hand_repository.side_effect = Exception(
        "Unexpected DB error"
    )  # Simulate error

    response = client.get("/api/v1/hands/hand123", cookies={"user_id": "valid_user"})

    assert response.status_code == 500
    assert "Error retrieving hand" in response.json()["detail"]
