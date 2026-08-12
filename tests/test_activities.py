"""Tests for the GET /activities endpoint"""
import pytest


def test_get_activities_returns_dict(client):
    """Test that GET /activities returns a dictionary"""
    response = client.get("/activities")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)


def test_get_activities_has_expected_activities(client):
    """Test that all expected activities are returned"""
    expected_activities = [
        "Chess Club",
        "Programming Class",
        "Gym Class",
        "Basketball Team",
        "Swimming Club",
        "Art Studio",
        "Photography Club",
        "Mathletes",
        "Debate Society"
    ]
    
    response = client.get("/activities")
    activities = response.json()
    
    for activity in expected_activities:
        assert activity in activities


def test_get_activities_structure(client):
    """Test that each activity has the correct structure"""
    response = client.get("/activities")
    activities = response.json()
    
    for activity_name, activity_data in activities.items():
        assert "description" in activity_data
        assert "schedule" in activity_data
        assert "max_participants" in activity_data
        assert "participants" in activity_data
        assert isinstance(activity_data["participants"], list)


def test_get_activities_participant_counts(client):
    """Test that participant counts are correct"""
    response = client.get("/activities")
    activities = response.json()
    
    # Chess Club should have 2 participants
    assert len(activities["Chess Club"]["participants"]) == 2
    assert "michael@mergington.edu" in activities["Chess Club"]["participants"]
    
    # Basketball Team should have 0 participants
    assert len(activities["Basketball Team"]["participants"]) == 0
