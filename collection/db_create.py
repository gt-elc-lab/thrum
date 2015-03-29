from models import db, Post, Comment

try:
    print "successfully cleared the database"
    Comment.query.delete()
    Post.query.delete()
    db.create_all()
    print "successfully created a new database"
except Exception as e:
    print "Error"
    print str(e)