import pytest
import pytest_asyncio
from fastapi.testclient import TestClient  # Use TestClient instead of AsyncClient
from main import app
from database import get_session, Base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.pool import NullPool

DATABASE_URL = "postgresql+asyncpg://postgres:authenticate@localhost:5432/myblog"
test_engine = create_async_engine(DATABASE_URL, echo=True, future=True, poolclass=NullPool)
TestSessionLocal = async_sessionmaker(bind=test_engine, class_=AsyncSession, expire_on_commit=False)

@pytest_asyncio.fixture(scope="function")
async def test_db():
    """Sets up a test database session."""
    async with test_engine.begin() as conn:
        # Create all tables
        await conn.run_sync(Base.metadata.create_all)
    async with TestSessionLocal() as session:
        yield session
    async with test_engine.begin() as conn:
        # Drop all tables after the test
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture(scope="function")
def client(test_db):
    """Creates an HTTP client with the test database session."""
    def override_get_session():
        yield test_db

    app.dependency_overrides[get_session] = override_get_session

    with TestClient(app) as c:
        yield c

@pytest.mark.asyncio
async def test_create_post(client):
    response = client.post("/posts/", json={
        "title": "Test Title",
        "content": "Test Content",
        "author": "Test Author",
        "image_url": None,
        "video_url": None
    })
    assert response.status_code == 200
    assert response.json()["title"] == "Test Title"

@pytest.mark.asyncio
async def test_get_posts(client):
    response = client.get("/posts/")
    assert response.status_code == 200
    assert "total_posts" in response.json()

@pytest.mark.asyncio
async def test_get_post_not_found(client):
    response = client.get("/posts/999")
    assert response.status_code == 404

@pytest.mark.asyncio
async def test_update_post(client):
    create_response = client.post("/posts/", json={
        "title": "Test Title",
        "content": "Test Content",
        "author": "Test Author",
        "image_url": None,
        "video_url": None
    })
    post_id = create_response.json()["id"]
    
    response = client.put(f"/posts/{post_id}", json={"title": "Updated Title"})
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Title"

@pytest.mark.asyncio
async def test_delete_post(client):
    create_response = client.post("/posts/", json={
        "title": "Test Title",
        "content": "Test Content",
        "author": "Test Author",
        "image_url": None,
        "video_url": None
    })
    post_id = create_response.json()["id"]
    
    response = client.delete(f"/posts/{post_id}")
    assert response.status_code == 204