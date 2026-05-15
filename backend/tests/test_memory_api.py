from fastapi.testclient import TestClient

from app.main import app


def test_memory_crud_flow() -> None:
    client = TestClient(app)

    chat_resp = client.post(
        "/api/v1/chat",
        json={"user_id": "u1", "session_id": "s-memory", "message": "你好"},
    )
    assert chat_resp.status_code == 200

    list_resp = client.get("/api/v1/memory/s-memory")
    assert list_resp.status_code == 200
    items = list_resp.json()
    assert len(items) == 2

    message_id = items[0]["id"]
    update_resp = client.put(
        f"/api/v1/memory/s-memory/{message_id}",
        json={"content": "更新后的内容"},
    )
    assert update_resp.status_code == 200
    assert update_resp.json()["content"] == "更新后的内容"

    delete_resp = client.delete(f"/api/v1/memory/s-memory/{message_id}")
    assert delete_resp.status_code == 200
    assert delete_resp.json()["deleted"] is True
