import itertools
from flask import Flask, json, render_template, request, jsonify
from datetime import datetime, timedelta
from collection.models import Post, db
from analysis.tfidf import TFIDF
from analysis.timeseries import TimeSerializer
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
    return render_template('dashboard.html',
                            college=college,
                            colleges=Post.list_colleges(),
                            activity=hourly_data)

@app.route('/time')
def send_hourly_activity():
    college = request.args.get('college')
    serializer = TimeSerializer()
    today = serializer.today()
    yesterday = serializer.get_days_ago(1)
    posts = fetch_posts_by_date(college, today , yesterday)
    data = compute_hourly_activity(posts)
    return jsonify(data=data)

def compute_hourly_activity(posts):
    serializer = TimeSerializer()
    activity = []
    for post in posts:
        activity.append(post)
        for comment in post.comments:
            activity.append(comment)
    return  serializer.hourly_activity(activity)

def fetch_posts_by_date(college, start, stop): 
    return query.filter(Post.created.between(stop, start),
                         Post.college == college).all()
if __name__ == "__main__":
    app.run(debug=True)