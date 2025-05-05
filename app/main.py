from fastapi import FastAPI
from app.routes import order

app = FastAPI(
        title="Система управления службой доставки",
        description="Система управления службой доставки, основанная на фреймворке FastAPI",
)

app.include_router(order.router)