"""Shared pytest fixtures for API tests"""
import copy
import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def client():
    """Provide a TestClient for the FastAPI app"""
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    """Reset activities dict before and after each test to ensure isolation"""
    # Store original state
    original_activities = copy.deepcopy(activities)
    
    yield
    
    # Restore original state after test
    activities.clear()
    activities.update(original_activities)


@pytest.fixture
def sample_activity():
    """Provide a sample activity that exists in the database"""
    return "Basketball Team"


@pytest.fixture
def sample_email():
    """Provide a sample email for testing signup"""
    return "test.student@mergington.edu"


@pytest.fixture
def full_activity():
    """Provide an activity name that starts full"""
    return "Photography Club"  # max_participants: 10, currently empty


@pytest.fixture
def occupied_activity():
    """Provide an activity with existing participants"""
    return "Chess Club"  # Has 2 participants
