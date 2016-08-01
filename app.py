from flask import Flask, render_template, request
from wtforms import Form, TextAreaField, validators
import dill
import sqlite3
import os
#import numpy as np

# import required modules
#from sklearn.feature_extraction.text import TfidfVectorizer
#from sklearn.svm import LinearSVC

# import HashingVectorizer from local dir
from vectorizer import vect

app = Flask(__name__)

######## Preparing the Classifier
cur_dir = os.path.dirname(__file__)
clf = dill.load(open(os.path.join(cur_dir,
                 'dill_objects',
                 'classifier.dill'), 'rb'))
db = os.path.join(cur_dir, 'docclf_db.sqlite')

def classify(document):
    label = {0: 'computer', 1: 'science', 2: 'sports', 3: 'religion', 4: 'politics', 5: 'automobiles'}
    # So, first converting text data into vectors of numerical values using tf-idf to form feature vector
    X = vect.transform([document])
    #vectorizer = TfidfVectorizer()
    #X = vectorizer.fit_transform(Xtr)
    y = clf.predict(X)[0]
    return label[y]

def train(document, y):
    X = vect.transform([document])
    clf.fit(X, [y])

def sqlite_entry(path, document, y):
    conn = sqlite3.connect(path)
    c = conn.cursor()
    c.execute("INSERT INTO docclftb (text, label, date)"\
    " VALUES (?, ?, DATETIME('now'))", (document, y))
    conn.commit()
    conn.close()

######## Flask
class ReviewForm(Form):
    textcontent = TextAreaField('',
                                [validators.DataRequired(),
                                validators.length(min=50)])

@app.route('/')
def index():
    form = ReviewForm(request.form)
    return render_template('reviewform.html', form=form)

@app.route('/results', methods=['POST'])
def results():
    form = ReviewForm(request.form)
    if request.method == 'POST' and form.validate():
        text = request.form['textcontent']
        y = classify(text)
        return render_template('results.html',
                                content=text,
                                prediction=y)
    return render_template('reviewform.html', form=form)

@app.route('/thanks', methods=['POST'])
def feedback():
    feedback = request.form['feedback_button']
    text = request.form['text']
    prediction = request.form['prediction']

    inv_label = {'computer' : 0, 'science' : 1, 'sports' : 2, 'religion' : 3, 'politics' : 4,'automobiles' : 5}
    y = inv_label[prediction]
    if feedback == 'Incorrect':
        y = int(not(y))
    train(text, y)
    sqlite_entry(db, text, y)
    return render_template('thanks.html')

if __name__ == '__main__':
    app.run(debug=True)
