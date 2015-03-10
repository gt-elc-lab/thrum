from flask import Flask, json, render_template, request, jsonify
from collection.models import Post
from analysis.tfidf import TFIDF
from analysis.timeseries import TimeSerializer
app = Flask(__name__)

@app.route("/")
def index():
    return render_template('header.html')

@app.route('/search')
def search_results():
    pass

@app.route('/tfidf')
def do_tfidf():
    corpus = [post.text for post in  Post.query.all()]
    document = Post.query.all()[0].text
    tfidf = TFIDF(corpus)
    result =  tfidf.batch_tfidf(document)
    return jsonify(data=result)

@app.route('/time')
def hourly():
    data = [post for post in Post.query.filter_by(subreddit='ncsu')]
    serializer = TimeSerializer(data)
    hours = serializer.hourly();
    return jsonify(data=hours)

@app.route('/days')
def daily():
    data = [post for post in Post.query.filter_by(subreddit='ncsu')]
    serializer = TimeSerializer(data)
    hours = serializer.daily();
    return jsonify(data=hours)

if __name__ == "__main__":
    app.run(debug=True)