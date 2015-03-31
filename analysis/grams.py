import nltk
from nltk.collocations import *

class BiGramGenerator(object):

    def __init__(self):
        return

    def bigrams(corpus, frequency):
        tokens = nltk.wordpunct_tokenize(corpus)
        finder = BigramCollocationFinder.from_words(tokens)
        finder.apply_freq_filter(frequency)
        bigram_measures = nltk.collocations.BigramAssocMeasures()
        scored = finder.score_ngrams(bigram_measures.raw_freq)
        grams = sorted(bigram for bigram, score in scored) 
        return grams