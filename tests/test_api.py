from fastapi.testclient import TestClient

from app.api import app


client = TestClient(

    app

)


def test_health(

        db_session

):

    response = client.get(

        "/health"

    )

    assert response.status_code == 200

    data = response.json()

    assert "status" in data

    assert data["status"] == "ok"



def test_readings(

        db_session

):

    response = client.get(

        "/readings"

    )

    assert response.status_code == 200


    data = response.json()


    assert isinstance(

        data,

        list

    )


    if data:

        reading = data[0]

        assert "city" in reading

        assert "timestamp" in reading

        assert "temperature" in reading

        assert "wind_speed" in reading

        assert "weather_code" in reading



def test_events(

        db_session

):

    response = client.get(

        "/events"

    )

    assert response.status_code == 200


    data = response.json()


    assert isinstance(

        data,

        list

    )


    if data:

        event = data[0]

        assert "city" in event

        assert "event_type" in event

        assert "severity" in event

        assert "message" in event

        assert "timestamp" in event