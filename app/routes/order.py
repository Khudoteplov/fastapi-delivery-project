from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy import text
from sqlmodel import Session, select
from app.db import get_session
from ..schemas import schema_order

router = APIRouter(prefix="/orders", tags=["Управление заказами в БД"])


@router.get("/test-db", status_code=status.HTTP_200_OK)
def test_database(session: Session = Depends(get_session)):
    result = session.exec(select(text("'Hello world'"))).all()
    return result

@router.post("/", status_code=status.HTTP_201_CREATED,
        summary = "Добавить заказ")
def create_order(ordr: schema_order.Order, session: Session = Depends(get_session)):
    """
    Добавить заказ
    """
    new_order = schema_order.Order(
            x=ordr.x,
            y=ordr.y,
            amount=ordr.amount
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
                
