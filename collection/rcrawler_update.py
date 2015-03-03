import praw
import time
from pprint import pprint
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from rcrawler_declarative import Post, Comment, Base

engine = create_engine("mysql+mysqldb://root:rtrad@localhost/yaks")
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

r = praw.Reddit('PRAW Gatech subreddit monitor')
r.login()

subreddit = r.get_subreddit('gatech')
for submission in subreddit.get_new(limit=30):
    new_post = Post(id=submission.id, title=submission.title, text=submission.selftext.encode('utf-8'), url=submission.url, ups=submission.ups, downs=submission.downs)
    session.merge(new_post)
    session.commit()
    comments = praw.helpers.flatten_tree(submission.comments)
    for comment in comments:
        new_comment = Comment(id=comment.id, body=comment.body.encode('utf-8'), ups=comment.ups, downs=comment.downs, post=new_post)
        session.merge(new_comment)
        session.commit()