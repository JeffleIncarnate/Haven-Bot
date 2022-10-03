import asyncpg
from dotenv import load_dotenv
import os

load_dotenv()
connection_string = os.environ["CONNECTION_STRING"]


async def create_pool() -> asyncpg.Pool:
    pool = await asyncpg.create_pool(connection_string)
    return pool
