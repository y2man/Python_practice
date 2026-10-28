
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_blank_prompt_is_rejected():
    response = client.post(
        "/ask",
        json={"prompt": "   ", "conversation_id": "test-123"}
    )
    assert response.status_code == 422


def test_empty_prompt_and_invalie_conversationid_is_rejected():
    response = client.post(
        "/ask",
        json={"prompt": "", "conversation_id": "test-456"}
    )
    assert response.status_code == 422


def test_nonexistent_conversation_returns_404():
    response = client.get("/conversations/nonexistent-123")
    assert response.status_code == 404
    

def test_deleting_nonexistent_conversation_returns_404():
    response = client.delete("/conversations/nonexistent-456")

    assert response.status_code == 404
    




