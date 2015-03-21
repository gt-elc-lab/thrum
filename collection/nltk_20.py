from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from rcrawler_declarative import Post, Comment, Base, engine
import nltk
from nltk.probability import FreqDist
from nltk.corpus import stopwords

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

posts = session.query(Post).filter(Post.subreddit == 'gatech').all()
comments = []
for post in posts:
    comments = comments + session.query(Comment).filter(Comment.post == post).all()

text = [p.text.lower() for p in posts] + [c.body.lower() for c in comments]
text = ' '.join(text)
tokens = nltk.word_tokenize(text)
fdist = FreqDist(tokens)

print len(set(tokens))

class WordFrequency(object):

    def __init__(self):
        self.stopwords = stopwords.words('english')

    def word_frequencies(corpus):
        tokens = nltk.word_tokenize(corpus)
        text = nltk.Text(tokens)
        fd = nltk.FreqDist(text)
        return [{'word': word, 'count':count} for word, count in fd.items()]

    def fuse(documents):
        return "".join([word in document.split(" ") for document in documents])