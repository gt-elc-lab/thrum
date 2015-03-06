from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

DATABASE_URI = 'mysql://root:password@localhost/proto_thrum' 
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
db = SQLAlchemy(app)

class Post(db.Model):
    
    id = db.Column(db.String(10), primary_key=True)
    title = db.Column(db.String(10000), nullable=False)
    text = db.Column(db.String(10000), nullable=True)
    url = db.Column(db.String(1000), nullable=True)
    ups = db.Column(db.Integer, nullable=False)
    downs = db.Column(db.Integer, nullable=False)

    def __init__(self, id, title, text, url, ups, downs):
        self.id = id
        self.title  = title
        self.text = text
        self.url = url
        self.ups = ups
        self.downs = downs

    def __repr__(self):
        return '<Post {}>'.format(self.title)


class Comment(db.Model):

    id = db.Column(db.String(10), primary_key=True)
    body = db.Column(db.String(10000), nullable=True)
    ups = db.Column(db.Integer, nullable=False)
    downs = db.Column(db.Integer, nullable=False)
    post_id = db.Column(db.String(10), db.ForeignKey('post.id'))
    post = db.relationship(Post)
    
    def __init__(self, id, body, ups, downs, post_id, post):
        self.id = id
        self.body = body
        self.ups = ups
        self.downs = downs
        self.post_id = post_id
        self.post = post

    def __repr__(self):
        return '<Comment {}>'.format(self.body) 

