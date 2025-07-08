import asyncpg
import os
from app.app_logging import app_logger as logger

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres@localhost/lms")

class Database:
    def __init__(self):
        self.pool = None

    async def connect(self):
        try:
            self.pool = await asyncpg.create_pool(DATABASE_URL)
            logger.info("Database connection pool created.")
        except Exception as error:
            logger.error(f"Failed to create database pool: {error}")
            raise

    async def disconnect(self):
        if self.pool:
            await self.pool.close()
            logger.info("Database connection pool closed.")

    async def get_conn(self):
        if not self.pool:
            raise RuntimeError("Database pool is not initialized.")
        return await self.pool.acquire()

db = Database() 