import praw
import time
from models import db, Post, Comment
from config import SUBREDDITS, USERNAME, PASSWORD


def main():
    reddit = praw.Reddit('PRAW Gatech subreddit monitor')
    print "logging in"
    reddit.login(USERNAME, PASSWORD)
    print "logged in. about to scrape"
    for school, subreddit in SUBREDDITS.iteritems():
        print "scraping {} : {}".format(school, subreddit)
        posts = reddit.get_subreddit(subreddit)
        crawl_subreddit(posts.get_new(limit=30), school, subreddit)
    

def crawl_subreddit(posts, school, subreddit):
    for submission in posts:
        new_post = Post(id=submission.id, 
                        title=submission.title.encode('utf-8'),
                        text=submission.selftext.encode('utf-8'),
                        url=submission.url, 
                        ups=submission.ups, 
                        downs=submission.downs,
                        subreddit=subreddit,
                        college=school,
                        create_utc=submission.created_utc)
        db.session.merge(new_post)
        db.session.commit()
        comments = praw.helpers.flatten_tree(submission.comments)
        for comment in comments:
            if isinstance(comment, praw.objects.Comment):
                new_comment = Comment(id=comment.id, 
                                      body=comment.body.encode('utf-8'), 
                                      ups=comment.ups, 
                                      downs=comment.downs,
                                      post_id=submission.id,
                                      post=new_post,
                                      create_utc=submission.created_utc)
                db.session.merge(new_comment)
                db.session.commit()
            else:
                continue

if __name__ == '__main__':
    main()
    

