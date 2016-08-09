from flask import Flask, render_template, request
from wtforms import Form, TextAreaField, validators
import dill
import sqlite3
import os

# import HashingVectorizer from local dir
from vectorizer import vect

app = Flask(__name__)

# Preparing the Classifier
cur_dir = os.path.dirname(__file__)
clf = dill.load(open(os.path.join(cur_dir,
                 'dill_objects',
                 'classifier.dill'), 'rb'))
db = os.path.join(cur_dir, 'docclf.sqlite')

def classify(document):
    label = {0: 'computer', 1: 'science', 2: 'sports', 3: 'religion', 4: 'politics', 5: 'automobiles'}
    X = vect.transform([document])
    y = clf.predict(X)[0]
    return label[y]

def train(document, y):
    X = vect.transform([document])
    clf.fit(X, [y])

def sqlite_entry(path, document, y):
    conn = sqlite3.connect(path)
    conn.text_factory = str
    c = conn.cursor()
    c.execute("INSERT INTO docclf_db(content, category, date)  VALUES(?, ?, DATETIME('now'))", (document, y))
    conn.commit()
    conn.close()

# Flask App
class ReviewForm(Form):
    textcontent = TextAreaField('', [validators.DataRequired(), validators.length(min=50)])

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
def thanks():
    text = request.form['text']
    inv_label = {'computer' : 0, 'science' : 1, 'sports' : 2, 'religion' : 3, 'politics' : 4,'automobiles' : 5}
    label = request.form['label']
    label = label.lower()
    y = inv_label[label]
    #train(text, y)
    sqlite_entry(db, text, y)
    return render_template('thanks.html')

@app.route('/thanktoo', methods=['POST'])
def thanktoo():
    feedback = request.form['feedback_button']
    if feedback == 'Correct':
        return render_template('thanktoo.html')

@app.route('/feedbackform', methods=['POST'])
def feedbackform():
    feedback = request.form['feedback_button']
    text = request.form['text']
    
    if feedback == 'Incorrect':
        return render_template('feedbackform.html', content=text)
        
if __name__ == '__main__':
    app.run(debug=False)
