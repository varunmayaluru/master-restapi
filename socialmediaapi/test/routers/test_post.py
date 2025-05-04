import pytest
from httpx import AsyncClient


async def create_post(body: str, async_client: AsyncClient) -> dict:
    response = await async_client.post("/post", json={"body": body})
    response.raise_for_status()
    return response.json()


@pytest.fixture()
async def created_post(async_client: AsyncClient):
    return await create_post("Test Post", async_client)


@pytest.fixture()
async def created_comment(async_client: AsyncClient, created_post: dict):
    payload = {"body": "Test Comment", "post_id": created_post["id"]}
    response = await async_client.post("/comment", json=payload)
    response.raise_for_status()
    return response.json()


@pytest.mark.anyio
async def test_create_post(async_client: AsyncClient):
    response = await async_client.post("/post", json={"body": "Test Post"})
    assert response.status_code == 201
    data = response.json()
    assert data["body"] == "Test Post"
    assert isinstance(data["id"], int)


@pytest.mark.anyio
async def test_create_post_missing_data(async_client: AsyncClient):
    response = await async_client.post("/post", json={})
    assert response.status_code == 422


@pytest.mark.anyio
async def test_get_all_posts(async_client: AsyncClient, created_post: dict):
    response = await async_client.get("/post")
    assert response.status_code == 200
    assert created_post in response.json()


@pytest.mark.anyio
async def test_create_comment(async_client: AsyncClient, created_post: dict):
    response = await async_client.post(
        "/comment",
        json={"body": "Test Comment", "post_id": created_post["id"]},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["body"] == "Test Comment"
    assert data["post_id"] == created_post["id"]


@pytest.mark.anyio
async def test_get_comments_on_post(
    async_client: AsyncClient, created_post: dict, created_comment: dict
):
    response = await async_client.get(f"/post/{created_post['id']}/comment")
    assert response.status_code == 200
    assert created_comment in response.json()


@pytest.mark.anyio
async def test_get_post_with_comments(
    async_client: AsyncClient, created_post: dict, created_comment: dict
):
    response = await async_client.get(f"/post/{created_post['id']}")
    assert response.status_code == 200
    assert response.json() == {
        "post": created_post,
        "comments": [created_comment],
    }


@pytest.mark.anyio
async def test_get_missing_post_with_comments(async_client: AsyncClient):
    response = await async_client.get("/post/999")
    assert response.status_code == 404
