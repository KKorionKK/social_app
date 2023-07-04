from sqlalchemy.orm import Session
from models.user_post import Post, User
from internal.authorization import crud_get_user
from schemas.user_schema import UserUpdateSchema
from schemas.post_schema import PostUpdateSchema


async def crud_get_my_posts(db: Session, user: User):
    return db.query(Post).filter(Post.user_id == user.id).all()


async def crud_update_user(db: Session,
                           new_user: UserUpdateSchema, user: User):
    _user = await crud_get_user(email=user.email, db=db)
    _user.name = new_user.name
    _user.surname = new_user.surname
    _user.email = new_user.email
    _user.password = new_user.password
    db.commit()
    db.refresh(_user)
    return _user


async def check_is_my_post(db: Session,
                           user: User, post_id: int) -> Post | bool:
    my_post = db.query(Post).filter(Post.user_id == user.id,
                                    Post.id == post_id).first()
    if my_post:
        return my_post
    else:
        return False


async def crud_delete_post_by_id(db: Session, user: User, post_id: int):
    post = await check_is_my_post(db=db, post_id=post_id, user=user)
    if post:
        db.delete(post)
        db.commit()
        db.refresh(post)
        return {'message': 'Post has been deleted'}
    else:
        return {'message': 'There is no your post like that :('}


async def crud_update_post_by_id(db: Session,
                                 user: User, new_post: PostUpdateSchema):
    post = await check_is_my_post(db=db, post_id=new_post.id, user=user)
    if post:
        post.header = new_post.header
        post.description = new_post.description
        db.commit()
        db.refresh(post)
        return post
