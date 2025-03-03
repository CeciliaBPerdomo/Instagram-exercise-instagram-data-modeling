import os
import sys
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, relationship
from sqlalchemy import create_engine, ForeignKey
from eralchemy2 import render_er

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(nullable=False)
    firstname: Mapped[str] = mapped_column(nullable=False) 
    lastname: Mapped[str] = mapped_column(nullable=False)
    mail: Mapped[str] = mapped_column(nullable=False)

    # Relación con Post (un usuario puede tener muchos posts)
    posts = relationship("Post", back_populates="user", cascade="all, delete-orphan")

    # Relación con Comment (un usuario puede tener muchos comentarios)
    comments = relationship("Comment", back_populates="user", cascade="all, delete-orphan")

    # Relación con Follower (un usuario puede seguir a muchos usuarios)
    followers = relationship("Follower", back_populates="user_from", cascade="all, delete-orphan")
    following = relationship("Follower", back_populates="user_to", cascade="all, delete-orphan")
    
class Post(Base):
    __tablename__ = 'post'
    id: Mapped[int] = mapped_column(primary_key=True)
    userid: Mapped[int] = mapped_column(ForeignKey('user.id'))

    # Relación con User
    user = relationship("User", back_populates="posts")

    # Relación con Comment (un post puede tener muchos comentarios)
    comments = relationship("Comment", back_populates="post", cascade="all, delete-orphan")

    # Relación con Media (un post puede tener muchos media)
    media = relationship("Media", back_populates="post", cascade="all, delete-orphan")

class Comment(Base):
    __tablename__ = 'comment'
    id: Mapped[int] = mapped_column(primary_key=True)
    comment: Mapped[str] = mapped_column(nullable=False)
    postid: Mapped[int] = mapped_column(ForeignKey('post.id'))
    authorid: Mapped[int] = mapped_column(ForeignKey('user.id'))

    # Relación con Post 
    post = relationship("Post", back_populates="comments")
    # Relación con User
    user = relationship("User", back_populates="comments")
    # Relacion con media
    media = relationship("Media", back_populates="comment", cascade="all, delete-orphan")

class Media(Base):
    __tablename__ = 'media'
    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str] = mapped_column(nullable=False)
    url: Mapped[str] = mapped_column(nullable=False)
    postid: Mapped[int] = mapped_column(ForeignKey('post.id'))

    # Relación con Post
    post = relationship("Post", back_populates="media", cascade="all, delete-orphan")


class Follower(Base):
    __tablename__ = 'follower'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_from_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    user_to_id: Mapped[int] = mapped_column(ForeignKey('user.id'))

    # Relación con User
    user_from = relationship("User", foreign_keys=[user_from_id])
    user_to = relationship("User", foreign_keys=[user_to_id])

## Draw from SQLAlchemy base
try:
    result = render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem genering the diagram")
    raise e
