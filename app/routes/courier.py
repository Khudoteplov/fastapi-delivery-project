from fastapi import APIRouter, status, Depends, HTTPException
from sqlmodel import Session, select
from app.db import get_session
from ..schemas import schema_user
from sqlalchemy.exc import IntegrityError
from psycopg2.errors import UniqueViolation
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from fastapi.security import OAuth2PasswordBearer
from ..auth import auth_handler
from app.config import settings
from datetime import timedelta
from typing import Annotated


router = APIRouter(prefix="/courier-status", tags=["Обновление состояния курьера"])

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
    else:
        current_courier.current_number = number
        session.commit()
        session.refresh(current_courier)
        return current_courier

