from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)


def test_rate_limit_single_ip() -> None:
    for _ in range(3):
        response = client.get("/")
        assert response.status_code == 200

    response = client.get("/")
    assert response.status_code == 429


def test_rate_limit_multiplt_ip() -> None:
    ip_names = ["ip1", "ip2", "ip3"]

    for ip in ip_names:
        headers =   {'X-Forwarded-For': ip}

        for _ in range(3):
            response = client.get("/", headers=headers)
            assert response.status_code == 200

        response = client.get("/", headers=headers)
        assert response.status_code == 429
