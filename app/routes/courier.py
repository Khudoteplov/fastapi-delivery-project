from typing import Annotated
from fastapi import (APIRouter, status, Depends, HTTPException)
from sqlmodel import Session, select
from app.db import get_session
from ..schemas import (schema_user, schema_order)
from ..auth import auth_handler

def distance(x1, y1, x2, y2):
    return ((x1-x2)**2+(y1-y2)**2)**0.5

router = APIRouter(prefix="/courier-status",
        tags=["Навигация и обновления состояния курьера"])

@router.patch("/location", status_code=status.HTTP_200_OK)
def update_location(x:float, y:float,
        current_courier: Annotated[schema_user.Courier,
            Depends(auth_handler.get_current_courier)],
        session: Session = Depends(get_session)):
    current_courier.x = x
    current_courier.y = y
    session.commit()
    session.refresh(current_courier)
    return current_courier

@router.patch("/number", status_code=status.HTTP_200_OK)
def update_number(number: int,
        current_courier: Annotated[schema_user.Courier,
            Depends(auth_handler.get_current_courier)],
        session: Session = Depends(get_session)):
    if number > current_courier.max_number or number < 0:
        raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Number out of range"
                )
    current_courier.current_number = number
    session.commit()
    session.refresh(current_courier)
    return current_courier

@router.get("/", status_code=status.HTTP_200_OK,
        response_model = schema_order.Order,
        summary = "Получить цель")
def get_target(current_courier: Annotated[schema_user.Courier,
            Depends(auth_handler.get_current_courier)],
            session: Session = Depends(get_session)):
    orders = session.exec(select(schema_order.Order).where(
        schema_order.Order.amount <= current_courier.current_number)).all()
    if orders is None or len(orders) == 0:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail="No orders available. Return to the storehouse"
        )
    curr_x = current_courier.x
    curr_y = current_courier.y
    k = 0
    min_d = distance(curr_x, curr_y, orders[0].x, orders[0].y)

    for i in range(len(orders)):
        t = distance(curr_x, curr_y, orders[i].x, orders[i].y)
        if t < min_d:
            min_d = t
            k = i
    return orders[k]
