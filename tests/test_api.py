from fastapi.testclient import TestClient

from change_lens.api import app

client = TestClient(app)


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_compare_validation_rejects_empty_content() -> None:
    response = client.post(
        "/v1/compare",
        json={
            "before": {"name": "old", "content": ""},
            "after": {"name": "new", "content": "content"},
        },
    )
    assert response.status_code == 422


def test_compare_endpoint_returns_evidence() -> None:
    response = client.post(
        "/v1/compare",
        json={
            "before": {"name": "old", "content": "# Access\nUse passwords."},
            "after": {"name": "new", "content": "# Access\nUse passkeys."},
        },
    )
    assert response.status_code == 200
    assert response.json()["evaluation"]["citation_coverage"] == 1.0
