from sqlalchemy.orm import Session
from models.user_post import Post, User, Like, Dislike
from schemas.post_schema import PostCreateSchema

from fastapi import status, HTTPException

existence_exception = HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='This post does not exist',
            )

repeat_exception = HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='You already rated this post',
            )


async def crud_create_post(post: PostCreateSchema, db: Session, user: User):
    _post = Post(**post.dict(), user_id=user.id)
    db.add(_post)
    db.commit()
    db.refresh(_post)

    return _post


async def crud_get_all_posts(db: Session):
    return db.query(Post).all()


async def crud_get_post_by_id(db: Session, post_id: int):
    post = db.query(Post).filter(Post.id == post_id).first()
    if post:
        return post
    else:
        return False


async def crud_check_self_faggot(db: Session, post_id: int, user: User):
    post = db.query(Post).filter(Post.id == post_id).first()
    if post.user_id == user.id:
        return False
    else:
        return True


async def check_like(db: Session, post_id: int, user: User):
    like = db.query(Like).filter(Like.post_id == post_id,
                                 Like.user_id == user.id).first()
    if like:
        return True
    else:
        return False


async def check_dislike(db: Session, post_id: int, user: User):
    dislike = db.query(Dislike).filter(Dislike.post_id == post_id,
                                       Dislike.user_id == user.id).first()
    if dislike:
        return True
    else:
        return False


async def get_like(db: Session, post_id: int, user: User):
    return db.query(Like).filter(Like.post_id == post_id,
                                 Like.user_id == user.id).first()


async def get_dislike(db: Session, post_id: int, user: User):
    return db.query(Dislike).filter(Dislike.post_id == post_id,
                                    Dislike.user_id == user.id).first()


async def crud_like_post(db: Session, post_id: int, user: User):
    post = await crud_get_post_by_id(db=db, post_id=post_id)
    if post:
        if await check_like(db=db, post_id=post_id, user=user):
            return repeat_exception
        elif await check_dislike(db=db, post_id=post_id, user=user):
            like = Like(user_id=user.id, post_id=post_id)
            dislike = await get_dislike(db=db, post_id=post_id, user=user)
            db.add(like)
            db.delete(dislike)
            db.commit()
            db.refresh(like)
            return post
        else:
            like = Like(user_id=user.id, post_id=post_id)
            db.add(like)
            db.commit()
            db.refresh(like)
            return post
    else:
        return existence_exception


async def crud_dislike_post(db: Session, post_id: int, user: User):
    post = await crud_get_post_by_id(db=db, post_id=post_id)
    if post:
        if await check_dislike(db=db, post_id=post_id, user=user):
            return repeat_exception
        elif await check_like(db=db, post_id=post_id, user=User):
            like = await get_like(db=db, post_id=post_id, user=user)
            dislike = Dislike(user_id=user.id, post_id=post_id)
            db.delete(like)
            db.add(dislike)
            db.commit()
            db.refresh(dislike)
            return post
        else:
            dislike = Dislike(user_id=user.id, post_id=post_id)
            db.add(dislike)
            db.commit()
            db.refresh(dislike)
            return post
    else:
        return existence_exception
