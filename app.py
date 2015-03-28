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

@app.route('/time')
def hourly_data():
    college = request.args.get('college')
    
if __name__ == "__main__":
    app.run(debug=True)