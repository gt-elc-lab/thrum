import itertools
from flask import Flask, json, render_template, request, jsonify
from datetime import datetime, timedelta
from collection.models import Post, db
from analysis.tfidf import TFIDF
from analysis.grams import BiGramGenerator
from analysis.d3_formatters import ForceLayout
from analysis.timeseries import TimeSerializer
from collection.nltk_20 import WordFrequency
app = Flask(__name__, static_url_path='/static')
query = db.session.query(Post)

@app.route('/')
def index():
    return render_template('home.html', colleges=Post.list_colleges())

@app.route('/dashboard/<college>')
def dashboard(college):
    serializer = TimeSerializer()
    today = serializer.today()
    yesterday = serializer.get_days_ago(1)
    posts = fetch_posts_by_date(college, today, yesterday)
    hourly_data = compute_hourly_activity(posts)
    word_cloud_data = compute_tfidf(posts[:40])
    # return jsonify(data=word_cloud_data)
    return render_template('dashboard.html',
                            college=college,
                            colleges=Post.list_colleges(),
                            activity=hourly_data,
                            word_cloud=word_cloud_data)

@app.route('/day')
def send_daily_activity():
    college = request.args.get('college')
    serializer = TimeSerializer()
    today = serializer.today()
    yesterday = serializer.get_days_ago(1)
    posts = fetch_posts_by_date(college, today , yesterday)
    data = compute_hourly_activity(posts)
    return jsonify(data=data)

@app.route('/week')
def send_weekly_activity():
    college = request.args.get('college')
    serializer = TimeSerializer()
    today = serializer.today()
    week_ago = serializer.get_weeks_ago(1)
    posts = fetch_posts_by_date(college, today, week_ago)
    data = compute_weekly_activity(posts)
    return jsonify(data=data)

@app.route('/wordcount')
def send_word_count():
    college = request.args.get('college')
    posts = fetch_todays_post(college)
    frequencies = compute_word_frequency(posts)
    return jsonify(data=frequencies)

@app.route('/bigrams/<college>/<word>')
def bigram_graph(college, word):
    posts = fetch_todays_post(college)
    corpus = fuse(posts_and_comments(posts), word)
    nodes, edges = bigram_graph(corpus)
    return jsonify(nodes=nodes, edges=edges)

def compute_hourly_activity(posts):
    serializer = TimeSerializer()
    activity = posts_and_comments(posts)
    return  serializer.hourly_activity(activity)

def compute_weekly_activity(posts):
    serializer = TimeSerializer()
    activity = posts_and_comments(posts)
    return serializer.weekly_activity(activity)

def posts_and_comments(posts):
    activity = []
    for post in posts:
        activity.append(post)
        for comment in post.comments:
            activity.append(comment)
    return activity

def fetch_posts_by_date(college, start, stop): 
    return query.filter(Post.created.between(stop, start),
                         Post.college == college).all()

def fetch_todays_post(college):
    today = datetime.now()
    yesterday = today - timedelta(days=1)
    return fetch_posts_by_date(college,today, yesterday)

def compute_word_frequency(posts):
    wf = WordFrequency()
    corpus = ""
    for item in posts:
        if isinstance(item, Post):
            cleaned = wf.remove_punctuation(item.text)
            corpus += cleaned
        else:
            cleaned = wf.remove_punctuation(item.body)
            corpus += cleaned
    frequencies = wf.word_frequencies(corpus)
    return sorted(frequencies,key=lambda x: x['value'], reverse=True)

def fuse(posts, word=None):
    corpus = ""
    for item in posts:
        if isinstance(item, Post):
            cleaned = WordFrequency.remove_punctuation(item.text)
            if word and  word in item.text:
                corpus += cleaned
        else:
            if word and word in item.body:
                cleaned = WordFrequency.remove_punctuation(item.body)
                corpus += cleaned
    return corpus

def bigram_graph(posts):
    bg_generator = BiGramGenerator()
    bigrams = bg_generator.bigrams(posts, 2)
    force_layout = ForceLayout()
    return force_layout.create_bigrams_graph(bigrams)

def compute_tfidf(posts):
    corpus = []
    for item in posts:
        if isinstance(item, Post):
            cleaned = WordFrequency.remove_punctuation(item.text)
            corpus.append(cleaned)
        else:
            cleaned = WordFrequency.remove_punctuation(item.body)
            corpus.append(cleaned)
    tfidf = TFIDF(corpus)
    r = []
    result = [tfidf.batch_tfidf(document, 100) for document in corpus]
    for document in result:
        for word in document:
            r.append(word)
    return r
if __name__ == "__main__":
    app.run(debug=True)