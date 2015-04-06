from models import db, Post, Comment

try:
    Comment.query.delete()
    Post.query.delete()
    print "successfully cleared the database"
except Exception as e:
    print str(e)
finally:
    db.create_all()
    print "successfully created a new database"