from fastapi import FastAPI
from contextlib import asynccontextmanager
from db import create_tables, delete_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    await delete_tables()
    print("Database is clear")
    await create_tables()
    print("Database is ready")
    yield
    print("Turning off")


