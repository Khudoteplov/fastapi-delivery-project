from fastapi import (APIRouter, status, Depends, HTTPException)
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError
from psycopg2.errors import UniqueViolation
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from datetime import timedelta
from app.db import get_session
from ..schemas import schema_user
from ..auth import auth_handler
from app.config import settings

router = APIRouter(prefix="/auth", tags=["Безопасность"])

@router.post("/signup", status_code=status.HTTP_201_CREATED,
             response_model=int,
             summary = 'Добавить пользователя')
def create_user(user: schema_user.User,
                session: Session = Depends(get_session)):
    new_user = schema_user.User(
        name=user.name,
        email=user.email,
        password=auth_handler.get_password_hash(user.password),
        x=user.x,
        y=user.y
    )
    try:
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
        return new_user.user_id
    except IntegrityError as e:
        assert isinstance(e.orig, UniqueViolation)
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"User with email {user.email} already exists"
        ) from e

@router.post("/courier/signup", status_code=status.HTTP_201_CREATED,
             response_model=int,
             summary = 'Добавить курьера')
def create_courier(courier: schema_user.Courier,
                session: Session = Depends(get_session)):
    new_courier = schema_user.Courier(
        name=courier.name,
        email=courier.email,
        password=auth_handler.get_password_hash(courier.password),
        max_number=courier.max_number
    )
    try:
        session.add(new_courier)
        session.commit()
        session.refresh(new_courier)
        return new_courier.courier_id
    except IntegrityError as e:
        assert isinstance(e.orig, UniqueViolation)
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Courier with email {courier.email} already exists"
        ) from e




@router.post("/login", status_code=status.HTTP_200_OK,
             summary = 'Вход в систему для клиентов')
def user_login(login_attempt_data: OAuth2PasswordRequestForm = Depends(),
               db_session: Session = Depends(get_session)):
    statement = (select(schema_user.User)
                 .where(schema_user.User.email == login_attempt_data.username))
    existing_user = db_session.exec(statement).first()

    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"User {login_attempt_data.username} not found"
        )

    if auth_handler.verify_password(
            login_attempt_data.password,
            existing_user.password):
        access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
        access_token = auth_handler.create_access_token(
            data={"sub": login_attempt_data.username},
            expires_delta=access_token_expires
        )
        return {
            "access_token": access_token,
            "token_type": "bearer"
        }
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"Wrong password for user {login_attempt_data.username}"
    )


@router.post("/courier/login", status_code=status.HTTP_200_OK,
             summary = 'Вход в систему для курьеров')
def courier_login(login_attempt_data: OAuth2PasswordRequestForm = Depends(),
               db_session: Session = Depends(get_session)):
    statement = (select(schema_user.Courier)
                 .where(schema_user.Courier.email == login_attempt_data.username))
    existing_user = db_session.exec(statement).first()

    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Courier {login_attempt_data.username} not found"
        )

    if auth_handler.verify_password(
            login_attempt_data.password,
            existing_user.password):
        access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
        access_token = auth_handler.create_access_token(
            data={"sub": login_attempt_data.username},
            expires_delta=access_token_expires
        )
        return {
            "access_token": access_token,
            "token_type": "bearer"
        }
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"Wrong password for courier {login_attempt_data.username}"
    )
