"""Tests for the root endpoint GET /"""
import pytest


def test_root_redirect(client):
    """Test that GET / redirects to /static/index.html"""
    response = client.get("/", follow_redirects=False)
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_root_follow_redirect(client):
    """Test that following the redirect returns 200"""
    response = client.get("/", follow_redirects=True)
    assert response.status_code == 200
