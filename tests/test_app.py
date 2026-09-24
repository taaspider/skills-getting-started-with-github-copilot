from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_signup_rejects_invalid_email_format():
    activity_name = "Soccer Club"
    invalid_email = "not-an-email"

    response = client.post(f"/activities/{activity_name}/signup?email={invalid_email}")

    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid email format"

    activities = client.get("/activities").json()
    assert invalid_email not in activities[activity_name]["participants"]


def test_unregister_participant_removes_email_from_activity():
    activity_name = "Chess Club"
    email = "student@example.com"

    client.post(f"/activities/{activity_name}/signup?email={email}")
    response = client.delete(f"/activities/{activity_name}/participants/{email}")

    assert response.status_code == 200
    data = response.json()
    assert data["message"] == f"Removed {email} from {activity_name}"

    activities = client.get("/activities").json()
    assert email not in activities[activity_name]["participants"]
