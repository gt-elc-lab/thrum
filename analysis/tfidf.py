import math
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

class TFIDF(object):
    """ Performs TFIDF against a given corpus"""
    
    def __init__(self, corpus):
        """
        Args:
           corpus: the corpus to perform tfidf with
        """
        self.corpus = corpus
        self.stopwords = stopwords.words('english')
        self.stopwords.append('I')
        self.stopwords.append('Im')

    def tfidf(self, word, document):
        """ Calculates tfidf for a word in the given document

        Args:
          word: the word to calculate tfidf for
          document: the document to check against

        Returns:
          tfidf score

        """
        return self._tf(word, document) * self._idf(word)

    def _tf(self, word, document):
        """ calculates term frequency

        Args:
          word: the word to calculate tfidf for
          document: the document to check against

        Returns:
          term frequency 
        """
        words = word_tokenize(document)
        return float(words.count(word)) / len(words)

    def _idf(self, word):
        """ Calculates inverse document frequency using the corpus

        Args:
          word: the word to calculate tfidf for

        Returns:
          inverse document frequency

        """
        num_appearances = self._documents_containing(word)
        return math.log(len(self.corpus) / 1 + num_appearances)

    def batch_tfidf(self, document, scale=1):
        """ Calculates tfidf for every word in the document

        Args:
            document: a list of documents

        """
        return [{'word': str(word) ,'value' : int(self.tfidf(word, document) * scale)} for word in word_tokenize(document)
        if word not in self.stopwords]

    def _documents_containing(self, word):
        """Determines how many documents in the document contain a word

        Args:
            word: the word to check for
        """
        return sum(1 for document in self.corpus if word in document)
