import nltk
import re
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from rcrawler_declarative import Post, Comment, Base, engine
from nltk.probability import FreqDist
from nltk.corpus import stopwords
from stop_words import get_stop_words
# Base.metadata.bind = engine

# DBSession = sessionmaker(bind=engine)
# session = DBSession()

# posts = session.query(Post).filter(Post.subreddit == 'gatech').all()
# comments = []
# for post in posts:
#     comments = comments + session.query(Comment).filter(Comment.post == post).all()

# text = [p.text.lower() for p in posts] + [c.body.lower() for c in comments]
# text = ' '.join(text)
# tokens = nltk.word_tokenize(text)
# fdist = FreqDist(tokens)

# print len(set(tokens))

class WordFrequency(object):

    def __init__(self):
        self.stopwords = get_stop_words('english') + stopwords.words('english')
        self.stopwords = [word.lower() for word in self.stopwords]

    def word_frequencies(self, text_glob):
        tokens = [word.lower() for word in nltk.word_tokenize(text_glob) 
                    if word not in self.stopwords]
        
        text = nltk.Text(tokens)
        fd = nltk.FreqDist(text)
        return [{'word': word, 'value':count} for word, count in fd.items()]

    def remove_punctuation(self, text):
        regex = re.compile('[^a-zA-Z0-9 -]')
        return regex.sub("", text)