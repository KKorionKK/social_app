from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from routes.authorization import get_current_user
from internal.posts import crud_get_all_posts, crud_create_post, crud_like_post
from internal.posts import crud_dislike_post, crud_check_self_faggot
from internal.database import Base, engine, SessionLocal
from schemas.post_schema import PostCreateSchema, PostSchema

from typing import Annotated, List
from models.user_post import User

posts_router = APIRouter(
    prefix='/posts',
    tags=['posts'],
    responses={404: {'description': 'Not Found'}},
)


Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@posts_router.get('/', response_model=List[PostSchema])
async def get_all_posts(current_user: Annotated[User, Depends(get_current_user)],
                        db: Session = Depends(get_db)):
    return await crud_get_all_posts(db=db)


@posts_router.post('/create_post', response_model=PostSchema)
async def create_post(current_user: Annotated[User, Depends(get_current_user)],
                      post: PostCreateSchema, db: Session = Depends(get_db)):
    return await crud_create_post(post=post, db=db, user=current_user)


@posts_router.post('/like/{post_id}')
async def add_like(current_user: Annotated[User, Depends(get_current_user)],
                   post_id: int, db: Session = Depends(get_db)):
    if await crud_check_self_faggot(db=db, post_id=post_id, user=current_user):
        return await crud_like_post(db=db, post_id=post_id, user=current_user)
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='You can not like your own post'
        )


@posts_router.post('/dislike/{post_id}')
async def add_dislike(current_user: Annotated[User, Depends(get_current_user)],
                   post_id: int, db: Session = Depends(get_db)):
    if await crud_check_self_faggot(db=db, post_id=post_id, user=current_user):
        return await crud_dislike_post(db=db, post_id=post_id, user=current_user)
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='You can not like your own post'
        )
