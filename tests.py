import unittest
from datetime import datetime
from analysis.tfidf import TFIDF
from collection.models import Post, Comment

class TFIDFTests(unittest.TestCase):

  def setUp(self):
    posts = Post.query.limit(200).all()
    comments = Comment.query.limit(200).all()
    self.corpus = posts+ comments
    self.tfidf = TFIDF(self.corpus)

  def testTFIDF(self):
    values = self.tfidf.get(Post)

if __name__ == '__main__':
    unittest.main()