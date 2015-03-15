import praw
from models import db, Post, Comment
from config import SUBREDDITS, USERNAME, PASSWORD
from datetime import datetime


def main():
    """
        Runs the crawler    
    """
    reddit = praw.Reddit('PRAW Gatech subreddit monitor')
    print "Logging in"
    reddit.login(USERNAME, PASSWORD)
    print "Logged in. Starting to scrape"
    for school, subreddit in SUBREDDITS.iteritems():
        print "Scraping {} : r/{}".format(school, subreddit)
        start = datetime.now()
        posts = reddit.get_subreddit(subreddit)
        num_posts, num_comments = crawl_subreddit(posts.get_new(limit=30), school, subreddit)
        duration = datetime.now() - start
        output = "Finished scraping {} : r/{} | {} posts {} comments | {} seconds"
        print output.format(school, subreddit, num_posts, num_comments, 
                                                        duration.seconds)
    print "Done"

def crawl_subreddit(posts, school, subreddit):
    """
        Args:
            posts: posts obtained from reddit
            school:  the name of the school
            subreddit: the name of the subreddit
        
        Returns:
            (num_posts, num_comments) : the number of posts and comments 
    """
    num_posts = 0
    num_comments = 0
    try: 
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
            num_posts += 1
            submission.replace_more_comments(limit=None, threshold=0)
            comments = praw.helpers.flatten_tree(submission.comments)
            for comment in comments:
                new_comment = Comment(id=comment.id, 
                                      body=comment.body.encode('utf-8'), 
                                      ups=comment.ups, 
                                      downs=comment.downs,
                                      post_id=submission.id,
                                      post=new_post,
                                      create_utc=submission.created_utc)
                db.session.merge(new_comment)
                db.session.commit()
                num_comments += 1
    except AssertionError as e:
        pass
       
    return (num_posts, num_comments)
            
if __name__ == '__main__':
    main()
    

