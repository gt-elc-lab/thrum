from flask import Flask, json, render_template, request, jsonify
from datetime import datetime, timedelta
from collection.models import Post, Comment, db
from collection.nltk_20 import WordFrequency
from analysis.tfidf import TFIDF
from analysis.grams import BiGramGenerator
from analysis.d3_formatters import ForceLayout
from analysis.timeseries import TimeSerializer
from collection.nltk_20 import WordFrequency
app = Flask(__name__, static_url_path='/static')
query = db.session.query(Post)

@app.route('/')
def index():
    colleges = Post.list_colleges()
    return render_template('home.html', colleges=colleges)


@app.route('/data/<tech>/<uga>/<word>')
def send_data(tech, uga, word):
    tech_posts = query_word_and_school(tech, word)
    uga_posts = query_word_and_school(uga, word)
    tech_results = bucketize(tech_posts, tech)
    uga_results = bucketize(uga_posts, uga)
    return jsonify(tech=tech_results,uga=uga_results)


def query_word_and_school(school, word):
    post_results = Post.query.whoosh_search(word).filter(Post.college==school)
    comments_results = Comment.query.whoosh_search(word).filter(Post.college==school)
    corpus = post_results.all() + comments_results.all()
    return corpus

def bucketize(corpus, school):
    serializer = TimeSerializer()
    return serializer.weekly_buckets(corpus, school)

if __name__ == "__main__":
    app.run(debug=True)
