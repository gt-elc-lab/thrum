from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from rcrawler_declarative import Post, Comment, Base, engine
import nltk
from nltk.probability import FreqDist

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

posts = session.query(Post).filter(Post.subreddit == 'gatech').all()
comments = []
for post in posts:
    comments = comments + session.query(Comment).filter(Comment.post == post).all()

text = [p.text.lower() for p in posts] + [c.body.lower() for c in comments]
text = ' '.join(text)
tokens = nltk.word_tokenize(text)
fdist = FreqDist(tokens)
print len(set(tokens))