from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime 

DATABASE_URI = 'mysql://root:password@localhost/proto_thrum' 
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
db = SQLAlchemy(app)

class Post(db.Model):
    """sqlalchemy Post object.

    Attributes:
      id (str):
      title (str):
      text (str):
      url (str):
      ups (int):
      downs (int):
      subreddit (str):
      college (str):
      time_stamp (datetime):
      created (datetime):
      modified (datetime):

    """
    id = db.Column(db.String(10), primary_key=True)
    title = db.Column(db.String(10000), nullable=False)
    text = db.Column(db.String(10000), nullable=True)
    url = db.Column(db.String(1000), nullable=True)
    ups = db.Column(db.Integer, nullable=False)
    downs = db.Column(db.Integer, nullable=False)
    subreddit = db.Column(db.String(1000), nullable=False)
    college = db.Column(db.String(1000), nullable=False)
    time_stamp = db.Column(db.DateTime, default=datetime.now())
    created = db.Column(db.DateTime, nullable=False)
    modified = db.Column(db.DateTime, default=datetime.now())


    def __init__(self, id, title, text, url, ups, downs, subreddit, college, create_utc):
         """
            Args:
              id (str):
              title (str):
              text (str):
              url (str):
              ups (int):
              downs (int):
              subreddit (str):
              college (str):
              time_stamp (datetime):
              created (datetime):
              modified (datetime):

        """
        self.id = id
        self.title  = title
        self.text = text
        self.url = url
        self.ups = ups
        self.downs = downs
        self.subreddit = subreddit
        self.college = college
        self.created = datetime.utcfromtimestamp(create_utc)

    def __repr__(self):
        """ String representation of a post object """
        return '<Post %s>' % self.title


class Comment(db.Model):
    """sqlalchemy Comment object.

    Attributes:
        id (str):
        body (str):
        ups (int):
        downs (int):
        post_id (str):
        post (sqlalchemy relationship):
        post_id (str):
        time_stamp (datetime):
        modified (datetime):
        created (datetime):
    """
    id = db.Column(db.String(10), primary_key=True)
    body = db.Column(db.String(10000), nullable=True)
    ups = db.Column(db.Integer, nullable=False)
    downs = db.Column(db.Integer, nullable=False)
    post_id = db.Column(db.String(10), db.ForeignKey('post.id'))
    post = db.relationship(Post)
    time_stamp = db.Column(db.DateTime, default=datetime.now())
    modified = db.Column(db.DateTime, default=datetime.now())
    created = db.Column(db.DateTime, nullable=False)
    
    def __init__(self, id, body, ups, downs, post_id, post, create_utc):
        """
        Args:
            id (str):
            body (str):
            ups (int):
            downs (int):
            post_id (str):
            post (sqlalchemy relationship):
            post_id (str):
            time_stamp (datetime):
            modified (datetime):
            created (datetime):
        """
        self.id = id
        self.body = body
        self.ups = ups
        self.downs = downs
        self.post_id = post_id
        self.post = post
        self.created = datetime.utcfromtimestamp(create_utc)

    def __repr__(self):
        """ String representation of a comment object"""
        return '<Comment %s>' % self.body 

