import pytest

@pytest.mark.asyncio
async def test_get_question_unauthenticated(async_client):
    response = await async_client.get("/api/v1/chat/question")
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_get_question_authenticated(authenticated_client):
    client, user = authenticated_client
    response = await client.get("/api/v1/chat/question")
    assert response.status_code == 200
    assert "content" in response.json()