import praw
import time
from pprint import pprint
from models import db, Post, Comment

def main():
    r = praw.Reddit('PRAW Gatech subreddit monitor')
    r.login('elc-gt', 'password')
    subreddit = r.get_subreddit('gatech')
    for submission in subreddit.get_new(limit=30):
        print "Getting submission:  {}".format(submission.title)
        new_post = Post(id=submission.id, 
                        title=submission.title, 
                        text=submission.selftext.encode('utf-8'),
                        url=submission.url, 
                        ups=submission.ups, 
                        downs=submission.downs)
        db.session.merge(new_post)
        db.session.commit()
        comments = praw.helpers.flatten_tree(submission.comments)
        for comment in comments:
            print "Getting Comment for: {}".format(submission.title)
            new_comment = Comment(id=comment.id, 
                                  body=comment.body.encode('utf-8'), 
                                  ups=comment.ups, 
                                  downs=comment.downs,
                                  post_id=submission.id ,
                                  post=new_post)
            db.session.merge(new_comment)
            db.session.commit()

if __name__ == '__main__':
    main()