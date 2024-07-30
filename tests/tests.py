import pytest
from fastapi.testclient import TestClient

@pytest.fixture
def provider_availability_payload():
    return {
        "provider_name": "Dr. Jekyll",
        "date": "2023-08-13",
        "start_time": "08:00",
        "end_time": "15:00"
    }

def test_submit_availability(test_client: TestClient, provider_availability_payload):
    response = test_client.post("/providers/availability", json=provider_availability_payload)
    assert response.status_code == 200