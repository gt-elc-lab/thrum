from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime 
import flask.ext.whooshalchemy as whoosh

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
    __tablename__ = 'post'
    __searchable__ = ['title','text']
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
    comments = db.relationship('Comment', backref='post', lazy='dynamic')

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

    @staticmethod
    def list_colleges():
        colleges = db.session.query(Post.college.distinct())
        return sorted([str(name[0]) for name in colleges.all()])


    def get_text(self):
      return self.text

    def __repr__(self):
        """ String representation of a post object """
        return '<Post %s>' % self.title

    def __hash__(self):
      return hash(self.id + str(self.created))

    def __eq__(self, other):
      return self.id == other.id


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
    __tablename__ = 'comment'
    __searchable__ = ['body']
    id = db.Column(db.String(10), primary_key=True)
    body = db.Column(db.String(10000), nullable=True)
    ups = db.Column(db.Integer, nullable=False)
    downs = db.Column(db.Integer, nullable=False)
    post_id = db.Column(db.String(10), db.ForeignKey('post.id'))
    time_stamp = db.Column(db.DateTime, default=datetime.now())
    modified = db.Column(db.DateTime, default=datetime.now())
    college = db.Column(db.String(1000), nullable=False)
    created = db.Column(db.DateTime, nullable=False)
    
    def __init__(self, id, body, ups, downs, post_id, create_utc, college):
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
        self.created = datetime.utcfromtimestamp(create_utc)
        self.college = college

    def get_text(self):
      return self.body 
      
    def __repr__(self):
        """ String representation of a comment object"""
        return '<Comment %s>' % self.body[:10]

    def __hash__(self):
      return hash(self.id + str(self.created))

    def __eq__(self, other):
      return self.id == other.id

whoosh.whoosh_index(app, Post)
whoosh.whoosh_index(app, Comment)