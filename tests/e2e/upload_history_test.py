import pytest
from fastapi.testclient import TestClient
from app.main import app
import io

client = TestClient(app)


@pytest.fixture
def sample_hand_history():
    """Returns a sample poker hand history as a string."""
    return """*********** # 1 **************
PokerStars Zoom Hand #254755246480:  Hold'em No Limit (€0.02/€0.05) - 2025/02/07 21:47:56 CET [2025/02/07 15:47:56 ET]
Table 'Asterope' 6-max Seat #1 is the button
Seat 1: Senefer (€4.01 in chips)
Seat 2: Mat22bcn (€9.48 in chips)
Seat 3: MakesMeRich (€5 in chips)
Seat 4: ScrappyDooLo (€5.43 in chips)
Seat 5: Nicoromero87 (€6.16 in chips)
Seat 6: vianney54 (€6.79 in chips)
Mat22bcn: posts small blind €0.02
MakesMeRich: posts big blind €0.05
*** HOLE CARDS ***
Dealt to Nicoromero87 [7c Js]
ScrappyDooLo: folds
Nicoromero87 is disconnected
Nicoromero87 has timed out while disconnected
Nicoromero87: folds
vianney54: folds
Senefer: raises €0.10 to €0.15
Mat22bcn: calls €0.13
MakesMeRich: folds
*** FLOP *** [Jd 4s Kh]
Mat22bcn: checks
Senefer: checks
*** TURN *** [Jd 4s Kh] [Ks]
Mat22bcn: bets €0.40
Senefer: folds
Uncalled bet (€0.40) returned to Mat22bcn
Mat22bcn collected €0.33 from pot
Mat22bcn: doesn't show hand
*** SUMMARY ***
Total pot €0.35 | Rake €0.02
Board [Jd 4s Kh Ks]
Seat 1: Senefer (button) folded on the Turn
Seat 2: Mat22bcn (small blind) collected (€0.33)
Seat 3: MakesMeRich (big blind) folded before Flop
Seat 4: ScrappyDooLo folded before Flop (didn't bet)
Seat 5: Nicoromero87 folded before Flop (didn't bet)
Seat 6: vianney54 folded before Flop (didn't bet)"""


def test_upload_valid_history_file(sample_hand_history):
    """Test that a valid poker hand history file is processed correctly."""
    test_user_id = "01a01v02-ed1f-11ef-901b-0ade7a4f7cd3"

    file_content = sample_hand_history.encode("utf-8")
    files = {"file": ("history.txt", io.BytesIO(file_content), "text/plain")}

    response = client.post(
        "/api/v1/hands",
        files=files,
        cookies={"user_id": test_user_id},
    )

    assert (
        response.status_code == 200
    ), f"Unexpected status code: {response.status_code}"
    assert response.json()["success"], "Response should be success"


def test_upload_invalid_file_format():
    """Test that an invalid file format returns a 400 error."""
    file_content = "This is a test file with an invalid format".encode("utf-8")
    files = {"file": ("history.csv", io.BytesIO(file_content), "text/csv")}

    response = client.post("/api/v1/hands", files=files)

    assert (
        response.status_code == 400
    ), f"Expected 400, but got {response.status_code}. Response: {response.text}"
    assert "Invalid file type" in response.json()["detail"]


def test_upload_empty_file():
    """Test uploading an empty file."""
    files = {"file": ("empty.txt", io.BytesIO(b""), "text/plain")}

    response = client.post("/api/v1/hands", files=files)

    assert response.status_code == 500  # It depends on how you handle empty files
    assert "Error reading file" in response.json()["detail"]


def test_upload_malformed_hand_history():
    """Test uploading a malformed hand history file."""
    file_content = "Malformed Hand History".encode("utf-8")
    files = {"file": ("malformed.txt", io.BytesIO(file_content), "text/plain")}

    response = client.post("/api/v1/hands", files=files)

    assert response.status_code in [
        200,
        500,
    ]  # Adjust based on expected handling of bad input
    assert response.json() or "detail" in response.json()
