import unittest
import nltk
from datetime import datetime
from datetime import timedelta
from analysis.tfidf import TFIDF
from analysis.ner import NER
from collection.models import Post, Comment

class TFIDFTests(unittest.TestCase):

  def setUp(self):
    self.corpus = fetch_data()
    self.tfidf = TFIDF(self.corpus)

  def testTFIDF(self):
    values = self.tfidf.get()
    for v, r in values:
        print v, r

  def testSchoolTFIDF(self):
    schools = Post.list_colleges()
    for school in schools:
        print ''
        print school
        print '_______________'
        corpus = fetch_data(college=school)
        results = TFIDF(corpus).get()[::-1]
        for v, r in results[:20]:
            print v, r

class NERTests(unittest.TestCase):

    def setUp(self):
        self.corpus = fetch_data()
        self.ner = NER(self.corpus)

    def testNER(self):
        data = "".join([item.get_text() for item in self.corpus])
        result = self.ner.named_entities(data)
        for v, r in result:
            if r in ['NN','JJ', 'NNS', 'JJR','RB','RBR']:
                print v , r
   
class TopicDetectionTests(unittest.TestCase):

    def setUp(self):
        self.corpus = fetch_data()
        self.tfidf_results = TFIDF(self.corpus).get()
        fused  = ''.join([item.get_text() for item in self.corpus])
        self.ner_results = NER(self.corpus).named_entities(fused)

    def testTopicDetection(self):
        tf = set([word[0] for word in self.tfidf_results if word[1] > 0.3])
        ner = set([word[0] for word in self.ner_results if word[1] in parts_of_speech])
        intersection = tf.intersection(ner)
        for word in intersection:
            print word
        recovered = recover_bigrams(tf, ner)
        for word in recovered:
            print word

parts_of_speech = set(['NN','JJ', 'NNS', 'JJR','RB','RBR'])

def fetch_data(college='Georgia Tech', limit=20):
    today = datetime.now()
    two_days_ago = today - timedelta(hours=48)
    posts = Post.query.filter(Post.college == college, Post.created.between(two_days_ago, today)).all()
    comments = []
    for post in posts: 
        for comment in post.comments:
            comments.append(comment)
    return posts + comments


def recover_bigrams(tfidf, named_entities):
    bigrams = set()
    for bigram in tfidf:
        first_word = bigram.split(" ")[0]
        if first_word in  named_entities:
            bigrams.add(bigram)
    return bigrams

if __name__ == '__main__':
    unittest.main()