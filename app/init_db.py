import asyncio
from app.db import db
from app.models import USER_TABLE_DDL
from app.app_logging import app_logger as logger

async def init_db():
    await db.connect()
    async with db.pool.acquire() as conn:
        try:
            await conn.execute(USER_TABLE_DDL)
            logger.info("Database schema initialized.")
        except Exception as error:
            logger.error(f"Failed to initialize schema: {error}")
            raise
    await db.disconnect()

if __name__ == "__main__":
    asyncio.run(init_db()) 