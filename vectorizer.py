from sklearn.feature_extraction.text import HashingVectorizer
import re
import os
import dill

cur_dir = os.path.dirname(__file__)
stop = dill.load(open(
                os.path.join(cur_dir,
                'dill_objects',
                'stopwords.dill'), 'rb'))

def tokenizer(text):
    text = re.sub('<[^>]*>', '', text)
    emoticons = re.findall('(?::|;|=)(?:-)?(?:\)|\(|D|P)',
                           text.lower())
    text = re.sub('[\W]+', ' ', text.lower()) \
                   + ' '.join(emoticons).replace('-', '')
    tokenized = [w for w in text.split() if w not in stop]
    return tokenized

vect = HashingVectorizer(decode_error='ignore',
                         n_features=36129,
                         preprocessor=None,
                         tokenizer=tokenizer)
