import math
from nltk.tokenize import word_tokenize

class TFIDF(object):
    
    def __init__(self, corpus):
        self.corpus = corpus

    def tfidf(self, word, document):
        return self._tf(word, document) * self._idf(word)

    def _tf(self, word, document):
        words = word_tokenize(document)
        return float(words.count(word)) / len(words)

    def _idf(self, word):
        num_appearances = self._documents_containing(word)
        return math.log(len(self.corpus) / 1 + num_appearances)

    def batch_tfidf(self, document):
        return [{word : self.tfidf(word, document) for word in word_tokenize(document)}]

    def _documents_containing(self, word):
        return sum(1 for document in self.corpus if word in document)
