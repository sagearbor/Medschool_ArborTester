import pytest

@pytest.mark.asyncio
async def test_get_question_unauthenticated(async_client):
    response = await async_client.get("/api/v1/chat/question")
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_get_question_authenticated(async_authenticated_client):
    client, user = await async_authenticated_client
    response = await client.get("/api/v1/chat/question")
    assert response.status_code == 200
    assert "content" in response.json()

def test_get_question_authenticated_sync(authenticated_client):
    client, user = authenticated_client
    response = client.get("/api/v1/chat/question")
    assert response.status_code == 200
    assert "content" in response.json()

def test_submit_answer_authenticated(authenticated_client):
    client, user = authenticated_client
    # First get a question
    question_response = client.get("/api/v1/chat/question")
    assert question_response.status_code == 200
    question_data = question_response.json()
    
    # Submit an answer
    response = client.post("/api/v1/chat/answer", json={
        "question_id": question_data["id"], 
        "user_answer": "Test answer"
    })
    assert response.status_code == 200
    assert "status" in response.json()
    assert "is_correct" in response.json()