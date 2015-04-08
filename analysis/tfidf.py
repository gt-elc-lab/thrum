import math
import re
import nltk
import string
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer


class TFIDF(object):

    def __init__(self, corpus):
        self.stemmer = PorterStemmer()
        self.corpus = corpus
        self.punctuation = (string.punctuation)
        self.tfidf = None

    def stem_tokens(self, tokens):
        stemmed = []
        for token in tokens:
            stemmed.append(self.stemmer.stem(token))
        return stemmed

    def tokenize(self, text):
        tokens = nltk.word_tokenize(text)
        stems = self.stem_tokens(tokens)
        return stems

    def compute(self, Post):
        token_dict = {}
        for document in self.corpus:
            text = ""
            if isinstance(document, Post):
                text = document.text.lower()
            else:
                text = document.body.lower()
            no_punctuation = "".join([ch for ch in text if ch not in self.punctuation])
            token_dict[document] = no_punctuation
        tfidf = TfidfVectorizer(tokenizer=self.tokenize, stop_words='english')
        tfidf.fit_transform(token_dict.values())
        self.tfidf = tfidf
        return self.tfidf

    def get(self, Post):
        tfidf = self.compute(Post)
        feature_names = tfidf.get_feature_names()
        words = []
        for item in self.corpus:
            response = None
            if isinstance(item, Post):
                response = tfidf.transform([item.text])
            else:
                response = tfidf.transform([item.body])
            for col in response.nonzero()[1]:
                words.append((feature_names[col], response[0, col]))
        words = sorted(words, key=lambda x: x[1])
        return words

