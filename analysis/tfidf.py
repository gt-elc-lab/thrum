import math
import re
import nltk
import string
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer


class TFIDF(object):

    def __init__(self, corpus, stemmer=PorterStemmer()):
        self.stemmer = stemmer
        self.corpus = corpus
        self.punctuation = (string.punctuation)
        self.tfidf = None

    def stem_tokens(self, tokens):
        stemmed = []
        for token in tokens:
            # stemmed.append(self.stemmer.stem(token))
            stemmed.append(token)
        return stemmed

    def tokenize(self, text):
        tokens = nltk.word_tokenize(text)
        stems = self.stem_tokens(tokens)
        return stems

    def compute(self, ngram_range=(1, 2)):
        token_dict = {}
        for document in self.corpus:
            text = document.get_text().lower()
            no_punctuation = "".join([ch for ch in text if ch not in self.punctuation])
            token_dict[document] = no_punctuation
        tfidf = TfidfVectorizer(tokenizer=self.tokenize, stop_words='english', ngram_range=ngram_range)
        tfidf.fit_transform(token_dict.values())
        self.tfidf = tfidf
        return self.tfidf

    def get(self):
        tfidf = self.compute()
        feature_names = tfidf.get_feature_names()
        words = []
        for item in self.corpus:
            response = tfidf.transform([item.get_text()])
            for col in response.nonzero()[1]:
                words.append((feature_names[col], response[0, col]))
        words = sorted(words, key=lambda x: x[1])
        return words

