"""Tests for the DELETE /activities/{activity_name}/unregister endpoint"""
import pytest


def test_unregister_success(client, occupied_activity):
    """Test successful unregister from an activity"""
    email = "michael@mergington.edu"  # Already in Chess Club
    
    response = client.delete(
        f"/activities/{occupied_activity}/unregister",
        params={"email": email}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert email in data["message"]
    assert occupied_activity in data["message"]


def test_unregister_removes_participant(client, occupied_activity):
    """Test that unregister actually removes participant from activity"""
    email = "michael@mergington.edu"
    
    # Get participants before unregister
    response_before = client.get("/activities")
    participants_before = response_before.json()[occupied_activity]["participants"]
    
    # Unregister
    client.delete(
        f"/activities/{occupied_activity}/unregister",
        params={"email": email}
    )
    
    # Get participants after unregister
    response_after = client.get("/activities")
    participants_after = response_after.json()[occupied_activity]["participants"]
    
    assert len(participants_after) == len(participants_before) - 1
    assert email not in participants_after


def test_unregister_increases_availability(client, occupied_activity):
    """Test that unregister increases available spots"""
    email = "michael@mergington.edu"
    
    response_before = client.get("/activities")
    max_participants = response_before.json()[occupied_activity]["max_participants"]
    spots_before = max_participants - len(response_before.json()[occupied_activity]["participants"])
    
    client.delete(
        f"/activities/{occupied_activity}/unregister",
        params={"email": email}
    )
    
    response_after = client.get("/activities")
    spots_after = response_after.json()[occupied_activity]["max_participants"] - len(response_after.json()[occupied_activity]["participants"])
    
    assert spots_after == spots_before + 1


def test_unregister_activity_not_found(client):
    """Test unregister returns 404 when activity doesn't exist"""
    response = client.delete(
        "/activities/Nonexistent Club/unregister",
        params={"email": "test@mergington.edu"}
    )
    
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_not_registered(client, sample_activity):
    """Test unregister returns 400 when student is not signed up"""
    email = "not.signed.up@mergington.edu"
    
    response = client.delete(
        f"/activities/{sample_activity}/unregister",
        params={"email": email}
    )
    
    assert response.status_code == 400
    assert "not signed up" in response.json()["detail"]


def test_unregister_then_signup_again(client, occupied_activity):
    """Test that a student can unregister and then sign up again"""
    email = "michael@mergington.edu"
    
    # Unregister
    response_unregister = client.delete(
        f"/activities/{occupied_activity}/unregister",
        params={"email": email}
    )
    assert response_unregister.status_code == 200
    
    # Try to sign up again
    response_signup = client.post(
        f"/activities/{occupied_activity}/signup",
        params={"email": email}
    )
    assert response_signup.status_code == 200
    
    # Verify they're back in the activity
    response = client.get("/activities")
    assert email in response.json()[occupied_activity]["participants"]


def test_unregister_multiple_participants(client, occupied_activity):
    """Test unregistering multiple participants from same activity"""
    emails = ["michael@mergington.edu", "daniel@mergington.edu"]
    
    for email in emails:
        response = client.delete(
            f"/activities/{occupied_activity}/unregister",
            params={"email": email}
        )
        assert response.status_code == 200
    
    # Verify both are removed
    response = client.get("/activities")
    participants = response.json()[occupied_activity]["participants"]
    
    for email in emails:
        assert email not in participants
