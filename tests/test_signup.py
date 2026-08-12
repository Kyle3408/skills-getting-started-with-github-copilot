"""Tests for the POST /activities/{activity_name}/signup endpoint"""
import pytest


def test_signup_success(client, sample_activity, sample_email):
    """Test successful signup for an activity"""
    response = client.post(
        f"/activities/{sample_activity}/signup",
        params={"email": sample_email}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert sample_email in data["message"]
    assert sample_activity in data["message"]


def test_signup_adds_participant_to_activity(client, sample_activity, sample_email):
    """Test that signup actually adds participant to the activity"""
    # Get activities before signup
    response_before = client.get("/activities")
    participants_before = response_before.json()[sample_activity]["participants"]
    
    # Sign up
    client.post(
        f"/activities/{sample_activity}/signup",
        params={"email": sample_email}
    )
    
    # Get activities after signup
    response_after = client.get("/activities")
    participants_after = response_after.json()[sample_activity]["participants"]
    
    assert len(participants_after) == len(participants_before) + 1
    assert sample_email in participants_after


def test_signup_decreases_availability(client, sample_activity):
    """Test that signup decreases available spots"""
    email = "new.student@mergington.edu"
    
    response_before = client.get("/activities")
    max_participants = response_before.json()[sample_activity]["max_participants"]
    spots_before = max_participants - len(response_before.json()[sample_activity]["participants"])
    
    client.post(
        f"/activities/{sample_activity}/signup",
        params={"email": email}
    )
    
    response_after = client.get("/activities")
    spots_after = response_after.json()[sample_activity]["max_participants"] - len(response_after.json()[sample_activity]["participants"])
    
    assert spots_after == spots_before - 1


def test_signup_activity_not_found(client, sample_email):
    """Test signup returns 404 when activity doesn't exist"""
    response = client.post(
        "/activities/Nonexistent Club/signup",
        params={"email": sample_email}
    )
    
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_already_registered(client, occupied_activity):
    """Test signup returns 400 when student already signed up"""
    # Chess Club has "michael@mergington.edu" already signed up
    email = "michael@mergington.edu"
    
    response = client.post(
        f"/activities/{occupied_activity}/signup",
        params={"email": email}
    )
    
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]


def test_signup_activity_full(client):
    """Test signup returns 400 when activity is at capacity"""
    activity = "Photography Club"  # max_participants: 10
    
    # Fill up the activity
    for i in range(10):
        email = f"student{i}@mergington.edu"
        client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )
    
    # Try to sign up one more
    response = client.post(
        f"/activities/{activity}/signup",
        params={"email": "overflow@mergington.edu"}
    )
    
    assert response.status_code == 400
    assert "Activity is full" in response.json()["detail"]


def test_signup_multiple_activities(client, sample_email):
    """Test that a student can sign up for multiple activities"""
    activities = ["Basketball Team", "Swimming Club", "Art Studio"]
    
    for activity in activities:
        response = client.post(
            f"/activities/{activity}/signup",
            params={"email": sample_email}
        )
        assert response.status_code == 200
    
    # Verify student is in all activities
    response = client.get("/activities")
    activities_data = response.json()
    
    for activity in activities:
        assert sample_email in activities_data[activity]["participants"]
