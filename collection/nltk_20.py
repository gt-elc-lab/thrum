from nltk.probability import FreqDist
from nltk.corpus import stopwords

class WordFrequency(object):

    def __init__(self):
        self.stopwords = stopwords.words('english')
        self.stopwords.append('I')

    def word_frequencies(self, text_glob):
        tokens = [word for word in nltk.word_tokenize(text_glob) 
                    if word not in self.stopwords]
        text = nltk.Text(tokens)
        fd = nltk.FreqDist(text)
        return [{'word': word, 'value':count} for word, count in fd.items()]

    @staticmethod
    def remove_punctuation(text):
        regex = re.compile('[^a-zA-Z0-9 ]')
        return regex.sub("", text)