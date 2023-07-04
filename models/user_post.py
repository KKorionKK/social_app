from internal.database import Base
from sqlalchemy import Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import List


class User(Base):
    __tablename__ = 'users'

    id = mapped_column(Integer, primary_key=True, index=True)
    name = mapped_column(String(64))
    surname = mapped_column(String(64))
    email = mapped_column(String(64))
    password = mapped_column(String(256))
    created = mapped_column(DateTime(timezone=False))

    posts: Mapped[List['Post']] = relationship(back_populates='user')
    liked_posts: Mapped[List['Like']] = relationship(back_populates='user')
    disliked_posts: Mapped[List['Dislike']] = relationship(back_populates='user')


class Post(Base):
    __tablename__ = 'posts'

    id = mapped_column(Integer, primary_key=True, index=True)
    header = mapped_column(String(64))
    description = mapped_column(String(256))
    created = mapped_column(DateTime(timezone=False))
    likes = relationship('Like', back_populates='post')
    dislikes = relationship('Dislike', back_populates='post')

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    user: Mapped['User'] = relationship(back_populates='posts')


class Like(Base):
    __tablename__ = 'likes'

    id = mapped_column(Integer, primary_key=True, index=True)
    user_id = mapped_column(Integer, ForeignKey('users.id'))
    post_id = mapped_column(Integer, ForeignKey('posts.id'))
    user = relationship('User', back_populates='liked_posts')
    post = relationship('Post', back_populates='likes')


class Dislike(Base):
    __tablename__ = 'dislikes'

    id = mapped_column(Integer, primary_key=True, index=True)
    user_id = mapped_column(Integer, ForeignKey('users.id'))
    post_id = mapped_column(Integer, ForeignKey('posts.id'))
    user = relationship('User', back_populates='disliked_posts')
    post = relationship('Post', back_populates='dislikes')
