from flask import Flask, json, render_template, request, jsonify
from datetime import datetime, timedelta
from collection.models import Post, Comment, db
from collection.nltk_20 import WordFrequency
from analysis.tfidf import TFIDF
from analysis.timeseries import TimeSerializer
app = Flask(__name__, static_url_path='/static')

@app.route("/")
def index():
    colleges = Post.list_colleges()
    return render_template('home.html', colleges=colleges)

@app.route('/dashboard/<college>')
def dashboard(college):
    query = db.session.query(Post)
    time_serializer = TimeSerializer()
    today = time_serializer.today()
    yesterday = time_serializer.get_days_ago(1)
    todays_posts = query.filter(Post.created.between(yesterday, today),
                         Post.college == college).all()
    hourly_data = time_serializer.hourly(todays_posts)
    wf =  WordFrequency()
    corpus = "".join([post.text for post in todays_posts])
    corpus = wf.remove_punctuation(corpus)
    word_cloud_data = wf.word_frequencies(corpus)

    tfidf = TFIDF([post.text for post in todays_posts])
    result = []
    for post in todays_posts:
        for r in tfidf.batch_tfidf(post.text):
            result.append(r)

    return render_template('dashboard.html', college=college,
                                            word_cloud_data=jsonify(data=word_cloud_data),
                                            tfidf_data=result)

@app.route('/dashboard/<college>/daily/<type>/')
def top_words_daily(college, type):
    time_serializer = TimeSerializer()
    today = time_serializer.today()
    yesterday = time_serializer.get_days_ago(1)
    wf =  WordFrequency()
    result = []
    if type == 'post':
        todays_posts = db.session.query(Post).filter(Post.created.between(yesterday, today),
                             Post.college == college).all()
        todays_posts_corpus = "".join([post.text for post in todays_posts])
        corpus = todays_posts_corpus
        corpus = wf.remove_punctuation(corpus)[:5*len(corpus)/100]
        tfidf = TFIDF(corpus)
        for post in todays_posts:
            for r in tfidf.batch_tfidf(post.text):
                result.append(r)
    elif type == 'title':
        todays_posts = db.session.query(Post).filter(Post.created.between(yesterday, today),
                             Post.college == college).all()
        todays_titles_corpus = "".join([post.title for post in todays_posts])
        corpus = todays_titles_corpus
        corpus = wf.remove_punctuation(corpus)[:5*len(corpus)/100]
        tfidf = TFIDF(corpus)
        for post in todays_posts:
            for r in tfidf.batch_tfidf(post.text):
                result.append(r)
    elif type == 'comment':
        todays_comments = db.session.query(Comment, Post).filter(Comment.post_id == Post.id,
                             Comment.created.between(yesterday, today),
                             Post.college == college).all()
        todays_comments_corpus = "".join([comment[0].body for comment in todays_comments])
        corpus = todays_comments_corpus
        corpus = wf.remove_punctuation(corpus)[:5*len(corpus)/100]
        tfidf = TFIDF(corpus)
        for post in todays_comments:
            for r in tfidf.batch_tfidf(post[0].body):
                result.append(r)

    word_cloud_data = wf.word_frequencies(corpus)
    return render_template('dashboard.html', college=college,
                                            word_cloud_data=jsonify(data=word_cloud_data),
                                            tfidf_data=result)

@app.route('/dashboard/<college>/weekly/<type>/')
def top_words_weekly(college, type):
    time_serializer = TimeSerializer()
    today = time_serializer.today()
    week_from_today = time_serializer.get_weeks_ago(1)
    wf =  WordFrequency()
    result = []
    if type == 'post':
        weekly_posts = db.session.query(Post).filter(Post.created.between(week_from_today, today),
                             Post.college == college).all()
        weekly_posts_corpus = "".join([post.text for post in weekly_posts])
        corpus = weekly_posts_corpus
        corpus = wf.remove_punctuation(corpus)[:5*len(corpus)/100]
        tfidf = TFIDF(corpus)
        for post in weekly_posts:
            for r in tfidf.batch_tfidf(post.text):
                result.append(r)
    elif type == 'title':
        weekly_posts = db.session.query(Post).filter(Post.created.between(week_from_today, today),
                             Post.college == college).all()
        weekly_titles_corpus = "".join([post.title for post in weekly_posts])
        corpus = weekly_titles_corpus
        corpus = wf.remove_punctuation(corpus)[:5*len(corpus)/100]
        tfidf = TFIDF(corpus)
        for post in weekly_posts:
            for r in tfidf.batch_tfidf(post.text):
                result.append(r)
    elif type == 'comment':
        weekly_comments = db.session.query(Comment, Post).filter(Comment.post_id == Post.id,
                             Comment.created.between(week_from_today, today),
                             Post.college == college).all()
        weekly_comments_corpus = "".join([comment[0].body for comment in weekly_comments])
        corpus = weekly_comments_corpus
        corpus = wf.remove_punctuation(corpus)[:5*len(corpus)/100]
        tfidf = TFIDF(corpus)
        for post in weekly_comments:
            for r in tfidf.batch_tfidf(post[0].body):
                result.append(r)

    word_cloud_data = wf.word_frequencies(corpus)
    return render_template('dashboard.html', college=college,
                                            word_cloud_data=jsonify(data=word_cloud_data),
                                            tfidf_data=result)

@app.route('/dashboard/<college>/alltime/<type>/')
def top_words_alltime(college, type):
    wf =  WordFrequency()
    result = []
    if type == 'post':
        alltime_posts = db.session.query(Post).filter(Post.college == college).all()
        alltime_posts_corpus = "".join([post.text for post in alltime_posts])
        corpus = alltime_posts_corpus
        corpus = wf.remove_punctuation(corpus)[:5*len(corpus)/100]
        tfidf = TFIDF(corpus)
        for post in alltime_posts:
            for r in tfidf.batch_tfidf(post.text):
                result.append(r)
    elif type == 'title':
        alltime_posts = db.session.query(Post).filter(Post.college == college).all()
        alltime_titles_corpus = "".join([post.title for post in alltime_posts])
        corpus = alltime_titles_corpus
        corpus = wf.remove_punctuation(corpus)[:5*len(corpus)/100]
        tfidf = TFIDF(corpus)
        for post in alltime_posts:
            for r in tfidf.batch_tfidf(post.title):
                result.append(r)
    elif type == 'comment':
        alltime_comments = db.session.query(Comment, Post).filter(Comment.post_id == Post.id,
                             Post.college == college).all()
        alltime_comments_corpus = "".join([comment[0].body for comment in alltime_comments])
        corpus = alltime_comments_corpus
        corpus = wf.remove_punctuation(corpus)[:5*len(corpus)/100]
        tfidf = TFIDF(corpus)
        for post in alltime_comments:
            for r in tfidf.batch_tfidf(post[0].body):
                result.append(r)
    word_cloud_data = wf.word_frequencies(corpus)
    return render_template('dashboard.html', college=college,
                                            word_cloud_data=jsonify(data=word_cloud_data),
                                            tfidf_data=result)

@app.route('/tfidf')
def do_tfidf():
    corpus = [post.text for post in  Post.query.all()]
    document = Post.query.all()[0].text
    tfidf = TFIDF(corpus)
    result =  tfidf.batch_tfidf(document)
    return jsonify(data=result)

@app.route('/hours')
def hourly():
    data = [post for post in Post.query.filter_by(subreddit='ncsu')]
    serializer = TimeSerializer(data)
    hours = serializer.hourly()
    return jsonify(data=hours)

@app.route('/days')
def daily():
    data = [post for post in Post.query.filter_by(subreddit='ncsu')]
    serializer = TimeSerializer(data)
    hours = serializer.daily()
    return jsonify(data=hours)

if __name__ == "__main__":
    app.run(debug=True)