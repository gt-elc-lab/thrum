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


@app.route('/data/')
def send_data():
    dropdown = Post.list_colleges()
    colleges = request.args.getlist('colleges')
    term = request.args.get('term')
    result = []
    for school in colleges:
        corpus = query_word(school, term)
        buckets = bucketize(corpus, school)
        if buckets:
            result += buckets
    return render_template('line_graph.html', colleges=dropdown,
                                              results=jsonify(data=result))


def query_word(college, word):
    post_results = Post.query.whoosh_search(word).filter(Post.college==college)
    comments_results = Comment.query.whoosh_search(word).filter(Comment.college==college)
    corpus = post_results.all() + comments_results.all()
    return corpus

def bucketize(corpus, school):
    serializer = TimeSerializer()
    return serializer.weekly_buckets(corpus, school)

if __name__ == "__main__":
    app.run(debug=True)
