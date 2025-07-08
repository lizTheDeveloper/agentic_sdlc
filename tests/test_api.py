import os
import pytest
import asyncio
from httpx import AsyncClient, ASGITransport
from app.main import app

import asyncpg
import pytest_asyncio

TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL", "postgresql://localhost/lms_test_db")

@pytest_asyncio.fixture(scope="session")
async def db_pool():
    pool = await asyncpg.create_pool(TEST_DATABASE_URL)
    yield pool
    await pool.close()

@pytest_asyncio.fixture(scope="session")
async def async_client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        yield client

@pytest.mark.asyncio
async def test_healthcheck(async_client):
    response = await async_client.get("/health")
    assert response.status_code == 200

# Add more tests for authentication, cohort, curriculum, event, assignment, submission, grading, and dashboard endpoints here.
# Example:
# @pytest.mark.asyncio
# async def test_create_cohort(async_client):
#     ... 