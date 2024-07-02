from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.db import create_tables, delete_tables
from app.router import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await delete_tables()
    print("Database is clear")
    await create_tables()
    print("Database is ready")
    yield
    print("Turning off")

app = FastAPI(lifespan=lifespan)
app.include_router(router)



 