####################################################
#
# REST API Unit Tests
#
# Responsibility
#
# Verify the behavior of REST API endpoints.
#
# Test Coverage
#
# • Health Endpoint
#
# • Weather Readings Endpoint
#
# • Weather Events Endpoint
#
# Validation Items
#
# • HTTP Status Code
#
# • JSON Response Structure
#
# • Expected Response Schema
#
# Dependencies
#
# • PyTest
#
# • FastAPI TestClient
#
# • Dependency Injection Override
#
# Processing Pipeline
#
# Create Test Client
#          ↓
# Send HTTP Request
#          ↓
# Receive JSON Response
#          ↓
# Validate Response
#
####################################################
import pytest

from fastapi.testclient import TestClient

from app.api import app

from app.api import get_db


####################################################
#
# API Client Fixture
#
# Responsibility
#
# Create a reusable FastAPI TestClient for
# API testing.
#
# The fixture overrides the production database
# dependency with a testing database session,
# ensuring that all API tests run in an isolated
# test environment.
#
# Lifecycle
#
# Setup
#      ↓
# Override get_db()
#      ↓
# Create TestClient
#      ↓
# Execute Test
#      ↓
# Restore Dependencies
#
####################################################

####################################################
#
# Test API Client Fixture
#
# Responsibility
#
# Configure a FastAPI TestClient that uses the
# testing database instead of the production
# database.
#
# Lifecycle
#
# Step 1.
# Override the database dependency.
#
# Step 2.
# Create the TestClient.
#
# Step 3.
# Execute API tests.
#
# Step 4.
# Remove the dependency override and restore
# the default application configuration.
#
####################################################

@pytest.fixture()

def api_client(

        db_session

):

    app.dependency_overrides[

        get_db

    ]=lambda: db_session


    yield TestClient(

        app

    )


    app.dependency_overrides={}



def test_health(

        api_client

):

    response=api_client.get(

        "/health"

    )

    assert response.status_code==200


    data=response.json()

    assert "status" in data

    assert data["status"]=="ok"



def test_readings(

        api_client

):

    response=api_client.get(

        "/readings"

    )

    assert response.status_code==200


    data=response.json()


    assert isinstance(

        data,

        list

    )


    if data:

        reading=data[0]


        assert "city" in reading

        assert "timestamp" in reading

        assert "temperature" in reading

        assert "wind_speed" in reading

        assert "weather_code" in reading



def test_events(

        api_client

):

    response=api_client.get(

        "/events"

    )

    assert response.status_code==200


    data=response.json()


    assert isinstance(

        data,

        list

    )


    if data:

        event=data[0]


        assert "city" in event

        assert "event_type" in event

        assert "severity" in event

        assert "message" in event

        assert "timestamp" in event