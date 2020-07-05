# Text preprocessing functions

# !pip install nltk
# nltk.download('stopwords')
# nltk.download('wordnet')
# nltk.download('punkt')

import string
import re
from nltk.corpus import stopwords, wordnet as wn

STOPWORDS = stopwords.words('english') + ['twitter', 'com']
PUNCT = list(string.punctuation) + ['’', '…']
URL_PATTERN = re.compile(r'https?://\S+|www\.\S+|pic\.twitter\S+')


def lowercase(col):
    """Convert words in <col> to lower case"""
    return col.str.lower()


def remove_new_lines(text):
    """Remove \n characters from <text>"""
    return text.replace('\n', ' ')


def remove_url(text):
    """Remove URLs from <text>"""
    return URL_PATTERN.sub(r'', text)


def remove_punctuations(text):
    """Remove punctuations from <text>"""
    for punctuation in PUNCT:
        text = text.replace(punctuation, ' ')
    return text


def remove_stopwords(text):
    """Remove the stopwords from <text>"""
    return " ".join([word for word in text.split() if word not in STOPWORDS])


def remove_digits(text):
    """Remove the digits from <text>"""
    return re.sub(r"\d", "", text)


def lemmatize_text(text):
    """Lemmatize words in <text>"""
    return " ".join([wn.morphy(word) if wn.morphy(word) is not None else word
                     for word in text.split()])


# Apply ALL the above functions to clean text in the passed column <col>

def clean_text(df, col):
    print("Cleaning text and storing it in new column 'processed_text'")
    df['processed_text'] = lowercase(df[col])\
        .apply(lambda text: remove_new_lines(text))\
        .apply(lambda text: remove_url(text))\
        .apply(lambda text: remove_punctuations(text))\
        .apply(lambda text: remove_stopwords(text))\
        .apply(lambda text: remove_digits(text))\
        .apply(lambda text: lemmatize_text(text))
    print('CLEANED! \n')
