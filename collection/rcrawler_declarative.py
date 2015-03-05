import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Post(Base):
    __tablename__ = 'post'
    id = Column(String(10), primary_key=True)
    title = Column(String(300), nullable=False)
    text = Column(String(10000), nullable=True)
    url = Column(String(1000), nullable=True)
    ups = Column(Integer, nullable=False)
    downs = Column(Integer, nullable=False)
    subreddit = Column(String(1000), nullable=False)

class Comment(Base):
    __tablename__ = 'comment'
    id = Column(String(10), primary_key=True)
    body = Column(String(10000), nullable=True)
    ups = Column(Integer, nullable=False)
    downs = Column(Integer, nullable=False)
    post_id = Column(String(10), ForeignKey('post.id'))
    post = relationship(Post)

engine = create_engine("mysql+mysqldb://root:rtrad@localhost/reddit")

Base.metadata.create_all(engine)