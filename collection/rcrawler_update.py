import praw
import time
from pprint import pprint
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from rcrawler_declarative import Post, Comment, Base
from config import SUBREDDITS

engine = create_engine("mysql+mysqldb://root:rtrad@localhost/reddit")
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

r = praw.Reddit('PRAW Gatech subreddit monitor')
r.login()

for subreddit in SUBREDDITS:
    print 'Scraping r/{}'.format(subreddit)
    subredditdata = r.get_subreddit(subreddit)
    for submission in subredditdata.get_new(limit=30):
        new_post = Post(id=submission.id, title=submission.title.encode('utf-8'), text=submission.selftext.encode('utf-8'), url=submission.url, ups=submission.ups, downs=submission.downs, subreddit=subreddit)
        session.merge(new_post)
        session.commit()
        comments = praw.helpers.flatten_tree(submission.comments)
        for comment in comments:
            new_comment = Comment(id=comment.id, body=comment.body.encode('utf-8'), ups=comment.ups, downs=comment.downs, post=new_post)
            session.merge(new_comment)
            session.commit()