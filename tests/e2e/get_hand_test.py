import pytest
import uuid
from fastapi import status
from fastapi.testclient import TestClient
from httpx import ASGITransport, AsyncClient
from app.main import app
from app.shared.infrastructure.di_container import get_dependency, mongo_db_client
from app.hand.domain.hand_repository import HandRepository
from tests.mocks.hand_mock import mock_hand

client = TestClient(app)


# Async fixture setup and teardown
@pytest.fixture(scope="module")
async def test_hand():
    # Ensure MongoDB is connected before tests run
    await mongo_db_client.connect_to_mongo()

    hand_id = mock_hand.id
    user_id = mock_hand.user_id
    hands_repository: HandRepository = get_dependency("hands_repository")

    # Create a test hand record
    await hands_repository.create(mock_hand)

    yield hand_id, user_id

    # Clean up after tests (async operation)
    await hands_repository.delete_all(mock_hand.user_id)

    # Close MongoDB connection after tests
    await mongo_db_client.close_mongo_connection()


@pytest.mark.anyio
async def test_get_hand_success(test_hand):
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        hand_id, user_id = test_hand
        response = await ac.get(
            f"/api/v1/hands/{hand_id}", cookies={"user_id": user_id}
        )
    assert response.status_code == 200  # Expect 200 OK status
    assert "hand" in response.json()
    assert response.json()["hand"]["id"] == hand_id
    assert response.json()["prev_hand_id"] is None
    assert response.json()["next_hand_id"] is None


@pytest.mark.anyio
async def test_get_hand_not_found():
    fake_hand_id = str(uuid.uuid4())
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.get(
            f"/api/v1/hands/{fake_hand_id}", cookies={"user_id": str(uuid.uuid4())}
        )
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.anyio
async def test_get_hand_missing_user_id():
    fake_hand_id = str(uuid.uuid4())
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.get(f"/api/v1/hands/{fake_hand_id}")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
