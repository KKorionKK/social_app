from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from routes.authorization import get_current_user
from internal.user import crud_get_my_posts, crud_update_user
from internal.user import crud_delete_post_by_id, crud_update_post_by_id
from internal.database import Base, engine, SessionLocal
from schemas.user_schema import UserUpdateSchema
from schemas.post_schema import PostUpdateSchema

from typing import Annotated
from models.user_post import User

user_router = APIRouter(
    prefix='/user',
    tags=['user'],
    responses={404: {'description': 'Not Found'}},
)


Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@user_router.get('/')
async def get_my_posts(current_user: Annotated[User, Depends(get_current_user)],
                       db: Session = Depends(get_db)):
    return await crud_get_my_posts(db=db, user=current_user)


@user_router.put('/update_user')
async def update_user(current_user: Annotated[User, Depends(get_current_user)],
                      new_user: UserUpdateSchema, db: Session = Depends(get_db)):
    return await crud_update_user(db=db, new_user=new_user, user=current_user)


@user_router.post('/delete_my_post')
async def delete_my_post(current_user: Annotated[User, Depends(get_current_user)],
                         post_id: int, db: Session = Depends(get_db)):
    return await crud_delete_post_by_id(db=db, user=current_user, post_id=post_id)


@user_router.put('/update_my_post')
async def update_my_post(current_user: Annotated[User, Depends(get_current_user)],
                         new_post: PostUpdateSchema, db: Session = Depends(get_db)):
    return await crud_update_post_by_id(db=db, user=current_user, new_post=new_post)
