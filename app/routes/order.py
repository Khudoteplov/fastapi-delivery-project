from typing import Annotated
from fastapi import (APIRouter, status, Depends, HTTPException)
from sqlmodel import Session, select
from ..auth import auth_handler
from ..schemas import (schema_order, schema_user)
from app.db import get_session


router = APIRouter(prefix="/orders", tags=["Управление заказами в БД"])


@router.post("/", status_code=status.HTTP_201_CREATED,
        summary = "Сделать заказ")
def create_order(amount: int,
        current_user: Annotated[schema_user.User,
            Depends(auth_handler.get_current_user)],
        session: Session = Depends(get_session)):
    """
    Сделать заказ
    """
    new_order = schema_order.Order(
            x=current_user.x,
            y=current_user.y,
            amount=amount
            )
    session.add(new_order)
    session.commit()
    session.refresh(new_order)
    return new_order

@router.get("/", status_code=status.HTTP_200_OK)
def read_orders(session: Session = Depends(get_session)):
    orders = session.exec(select(schema_order.Order)).all()
    if orders is None or len(orders) == 0:
        raise HTTPException(
                status_code=status.HTTP_204_NO_CONTENT,
                detail="List of orders is empty."
                )
    return orders

@router.delete("/", status_code=status.HTTP_200_OK)
def remove_order(order_id: int,
        session: Session = Depends(get_session)):
    to_del = session.query(schema_order.Order).filter(
            schema_order.Order.order_id == order_id)
#    if to_del is None:
#        raise HTTPException(
#                status_code=status.HTTP_204_NO_CONTENT,
#                detail=f"There is no order with ID {order_id}"
#                )
    to_del.delete()
    session.commit()
