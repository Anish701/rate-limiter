import pytest
from fastapi.testclient import TestClient

from src.main import app, rate_limiter

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_rate_limiter():
    rate_limiter.buckets.clear()


def test_rate_limit_single_ip() -> None:
    for _ in range(3):
        response = client.get("/")
        assert response.status_code == 200

    response = client.get("/")
    assert response.status_code == 429


def test_rate_limit_multiple_ips() -> None:
    ip_names = ["ip1", "ip2", "ip3"]

    for ip in ip_names:
        headers = {"X-Forwarded-For": ip}

        for _ in range(3):
            response = client.get("/", headers=headers)
            assert response.status_code == 200

        response = client.get("/", headers=headers)
        assert response.status_code == 429
