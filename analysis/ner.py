from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk import probability
from stop_words import get_stop_words
from nltk.tag import pos_tag

class NER(object):
    """ Performs Named Entity Recognition against a given corpus"""
    
    def __init__(self, corpus):
        self.corpus = corpus
        self.stopwords = get_stop_words('english') + stopwords.words('english')

    def tag_words(self, sentence):
        return pos_tag(sentence)

    def tokenize_sentences(self, corpus):
        sentences = sent_tokenize(corpus)
        return sentences
    
    def tokenize_words(self, sentence):
        words = word_tokenize(sentence)
        return words

    def named_entities(self, corpus, tag_prefix=""):
        sentences = self.tokenize_sentences(corpus)
        tagged_text = []
        for sentence in sentences:
            tagged_text = tagged_text + (self.tag_words(self.tokenize_words(sentence)))
        return [(word, tag) for (word, tag) in tagged_text if tag.startswith(tag_prefix)]