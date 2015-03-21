from flask import Flask, json, render_template, request, jsonify
from datetime import datetime, timedelta
from collection.models import Post, db
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
    yesterday = time_serializer.get_days_ago(30)
    todays_posts = query.filter(Post.created.between(yesterday, today),
                         Post.college == college).all()
    hourly_data = time_serializer.hourly(todays_posts)
    num_posts = len(todays_posts)
    num_comments = num_posts
    redditors = num_posts
    return render_template('dashboard.html', college=college,
                                            posts=num_posts,
                                            comments=num_comments,
                                            redditors=num_posts,
                                            hourly_data=hourly_data)

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