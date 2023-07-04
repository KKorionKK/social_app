from typing import Annotated
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from jose import JWTError, jwt
from passlib.context import CryptContext

from sqlalchemy.orm import Session

from schemas.user_schema import UserSchema
from schemas.user_schema import UserCreateSchema
from schemas.token_scheme import Token

from internal.authorization import crud_get_user, crud_create_user
from internal.database import Base, engine, SessionLocal
# openssl rand -hex 32 :)
SECRET_KEY = "49034da225c772f1477176257d60538c98e4a0e150122e8c80fb6a4c723810dd"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRATION_TIME = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/authorization/token")

auth_router = APIRouter(
    prefix='/authorization',
    tags=['authorization'],
    responses={404: {'description': 'Not Found'}},
)

Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_hashed_password(password):
    return pwd_context.hash(password)


async def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


async def get_user(session, username: str):
    return await crud_get_user(email=username, db=session)


async def authenticate_user(username: str, password: str,
                            session: Session = Depends(get_db)):
    user = await get_user(session, username)
    if not user:
        return False
    if not await verify_password(password, user.password):
        return False
    return user


async def create_access_token(data: dict,
                              expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)],
                           session: Session = Depends(get_db)):
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Coul not verify credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credential_exception
    except JWTError:
        raise credential_exception
    user = await get_user(session=session, username=username)
    if user is None:
        raise credential_exception
    return user


@auth_router.post('/token', response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                                 session: Session = Depends(get_db)):
    user = await authenticate_user(session=session, username=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRATION_TIME)
    access_token = await create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@auth_router.post('/register', response_model=UserSchema)
async def register_user(user: UserCreateSchema, session: Session = Depends(get_db)):
    user.password = await get_hashed_password(user.password)
    response = await crud_create_user(user=user, db=session)
    return response
