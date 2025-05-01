import nltk
from nltk.tokenize import word_tokenize
from nltk.stem.porter import PorterStemmer

nltk.download('punkt_tab')

stemmer = PorterStemmer()

def preprocess(text):
    tokens = word_tokenize(text.lower())
    stems = [stemmer.stem(word) for word in tokens]
    return " ".join(stems)