from app.models import Sessions, Scores, Signup, ClimateFeed
import pytest

@pytest.fixture
def mock_datetime():
    pass

def test_scores_model():
    scores = Scores(1, "7b25a87c-d2c8-49e3-83ac-88dcc1d94902", 4.5, 5.5, 3.5, 2.5, 4.5, 3.5, 0.5, 2.5, 3.5, 1.5, None)
    assert scores.scores_id == 1
    assert scores.session_id == "7b25a87c-d2c8-49e3-83ac-88dcc1d94902"
    assert scores.security == 4.5
    assert scores.conformity == 5.5
    assert scores.benevolence == 3.5
    assert scores.tradition == 2.5
    assert scores.universalism == 4.5
    assert scores.self_direction == 3.5
    assert scores.stimulation == 0.5
    assert scores.hedonism == 2.5
    assert scores.achievement == 3.5
    assert scores.power == 1.5
    assert scores.user_id == None

def test_sessions_model():
    session = Sessions("7b25a87c-d2c8-49e3-83ac-88dcc1d94902", "90210", "66.249.70.61")
    assert session.id == "7b25a87c-d2c8-49e3-83ac-88dcc1d94902"
    assert session.postal_code == "90210"
    assert session.ip_address == "66.249.70.61"

def test_signup_model():
    signup = Signup("test@signup.com", "7b25a87c-d2c8-49e3-83ac-88dcc1d94902")
    pass

def test_climate_feed():
    climateFeed = ClimateFeed()