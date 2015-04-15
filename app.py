import string
from flask import Flask, json, render_template, request, jsonify
from flask.ext.triangle import Triangle
from nltk.tokenize import sent_tokenize
from datetime import datetime, timedelta
from collection.models import Post, Comment, db
from collection.nltk_20 import WordFrequency
from analysis.tfidf import TFIDF
from analysis.grams import BiGramGenerator
from analysis.d3_formatters import ForceLayout
from analysis.timeseries import TimeSerializer
from analysis.ner import NER
from collection.nltk_20 import WordFrequency
app = Flask(__name__, static_url_path='')
Triangle(app)
query = db.session.query(Post)

@app.route('/')
def root():
    return render_template('index.html')

@app.route('/colleges')
def colleges():
    schools = Post.list_colleges()
    return jsonify(data=schools)

@app.route('/trending')
def trending():
    college = request.args.get('college')
    data = fetch_data(college)
    topics = detect_topics(data)
    return jsonify(data=topics)

@app.route('/posts')
def send_posts():
    college = request.args.get('college')
    term = request.args.get('term')
    posts = [item.get_text() for item in text_search(college, term)]
    return jsonify(data=posts)

@app.route('/usage')
def usage():
    college = request.args.get('college')
    term = request.args.get('term')
    posts = text_search(college, term)
    data  = cluster(posts)
    return jsonify(data=data)

@app.route('/content')
def content():
    college = request.args.get('college')
    term = request.args.get('term')
    posts = text_search(college, term)
    posts = [post.get_text() for post in posts]
    return jsonify(data=posts)

@app.route('/wordtree')
def wordtree():
    college = request.args.get('college')
    term = request.args.get('term')
    corpus = text_search(college, term)
    text = [item.get_text() for item in corpus]
    relevant = extract_relevant_sentences(term, text)
    return jsonify(data=relevant)

def extract_relevant_sentences(term, text):
    relevant = []
    for document in text:
        sentences = sent_tokenize(document)
        contains_word = [sentence for sentence in sentences if term in sentence]
        if contains_word:
            for s in contains_word:
                relevant.append([remove_punctionation(s)])
    return relevant

def remove_punctionation(text):
    return ''.join([ch for ch in text if ch not in string.punctuation])

def text_search(college, term):
    present = datetime.now()
    past = datetime.now() - timedelta(weeks=4)
    posts = Post.query.whoosh_search(term).filter(
        Post.college==college,
        Post.created.between(past, present)).all()
    comments = Comment.query.whoosh_search(term).filter(
        Comment.college==college,
        Comment.created.between(past, present)).all()
    return posts + comments

def cluster(posts):
    return TimeSerializer().daily_buckets(posts)  

def fetch_data(college, hours=24):
    today = datetime.now()
    two_days_ago = today - timedelta(hours=hours)
    posts = Post.query.filter(
        Post.college == college,
        Post.created.between(two_days_ago, today)).all()
    comments = []
    for post in posts: 
        for comment in post.comments:
            comments.append(comment)
    return posts + comments

def detect_topics(corpus):
    tfidf = TFIDF(corpus).get()
    relevant = set([word[0] for word in tfidf if word[1] > 0.4])
    return list(relevant)

if __name__ == "__main__":
    app.run(debug=True)
   


