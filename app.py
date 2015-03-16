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


@app.route('/timeseries/<college>')
def timeseries_dashboard(college):
    query = db.session.query(Post)
    now = datetime.now()
    yesterday = now - timedelta(days=2)
    two_weeks_ago = now - timedelta(weeks=2)
    posts = query.filter(Post.created.between(yesterday, now),
                         Post.college == college).all()
    current_data = TimeSerializer(posts).average_hourly(1) 
    posts = query.filter(Post.created.between(two_weeks_ago, yesterday)).all()
    historical_data = TimeSerializer(posts).average_hourly(14)
    return render_template('dashboard.html', college=college,
                                             colleges=Post.list_colleges(), 
                                             past_day=current_data,
                                             historical_data= historical_data)

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