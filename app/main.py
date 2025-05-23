from fastapi import FastAPI
from app.routes import (order, auth, courier)
from contextlib import asynccontextmanager
from app.db import init_database

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_database()
    yield           # <<< Uncomment if you need to create tables on app start


app = FastAPI(
    lifespan=lifespan,  # Uncomment if you need to create tables on app start
    title="Система управления службой доставки",
    description="Система управления службой доставки, основанная на фреймворке FastAPI",
)

app.include_router(order.router)
app.include_router(auth.router)
app.include_router(courier.router)
