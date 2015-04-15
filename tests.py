import unittest
import nltk
import json
from nltk.tokenize import word_tokenize
from datetime import datetime
from datetime import timedelta
from analysis.tfidf import TFIDF
from analysis.ner import NER
from collection.models import Post, Comment
from nltk.collocations import *

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
        print schools
        for school in schools:
            print ''
            print school
            print '_______________'
            corpus = fetch_data(college=school)
            results = TFIDF(corpus).get()
            results = [t for t in results if t[1] > 0.4]
            for v, r in results:
                print v, r
    
    def testPostTfidf(self):
        relevant = []
        for post in self.corpus:
            try:
                tf = TFIDF(post.get_text()).post_get()
                for r in tf:
                    if r[1] > 0.7:
                        relevant.append(r)
            except Exception as e:
                print str(e)
        for w, i in relevant:
            print w, i

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

def fetch_data(college='Georgia Tech', limit=None,days=2):
    today = datetime.now()
    two_days_ago = today - timedelta(days=days)
    if limit:
        posts = Post.query.limit(limit).all()
    else:
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