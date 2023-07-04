from sqlalchemy.orm import Session
from models.user_post import User
from schemas.user_schema import UserCreateSchema


async def crud_get_user(email: str, db: Session):
    user = db.query(User).filter(User.email == email).first()
    if user:
        return user


async def crud_create_user(user: UserCreateSchema, db: Session):
    if not await crud_get_user(email=user.email, db=db):
        _user = User(**user.dict())
        db.add(_user)
        db.commit()
        db.refresh(_user)
        return _user
    else:
        return False
