from flask import Flask, json, render_template, request, jsonify
from nltk.tokenize import sent_tokenize
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
        buckets = bucketize(corpus, school, term)
        if buckets:
            result += buckets
    return render_template('line_graph.html', colleges=dropdown,
                                              results=jsonify(data=result))

@app.route('/<college>/<word>/<time_stamp>')
def word_tree(college, word, time_stamp):
    corpus = query_interval(college, word, time_stamp)
    return jsonify(data=word_tree_data(corpus))

def query_word(college, word):
    post_results = Post.query.whoosh_search(word).filter(Post.college==college)
    comments_results = Comment.query.whoosh_search(word).filter(Comment.college==college)
    corpus = post_results.all() + comments_results.all()
    return corpus

def bucketize(corpus, school, term):
    serializer = TimeSerializer()
    return serializer.weekly_buckets(corpus, school, term)

def word_tree_data(posts):
    corpus = ""
    for post in posts:
        if isinstance(post, Post):
            corpus += post.title
            corpus += post.text
        if isinstance(post, Comment):
            corpus += post.body
    return sent_tokenize(corpus)

def query_interval(college, word, time_stamp):
    date = datetime.fromtimestamp(float(time_stamp) / 1000)
    week_before = date - timedelta(weeks=1)
    week_after = date + timedelta(weeks=1)
    posts = Post.query.whoosh_search(word).filter(Post.college==college, 
                                                Post.created.between(week_before, week_after))
    comments = Comment.query.whoosh_search(word).filter(Comment.college==college, 
                                                Comment.created.between(week_before, week_after))
    result = posts.all()  + comments.all()
    return result

if __name__ == "__main__":
    app.run(debug=True)
    # posts = Post.query.filter(Post.college=='Georgia Tech').all()[:300]
    # corpus = [post.text for post in posts]
    # text = "".join([p for p in corpus])
    # tf = TFIDF(corpus)
    # a=[]
    # for c in corpus:
    #     a+= tf.batch_tfidf(c)
    # a = sorted(a, key=lambda x:x['value'])
    # for word in a:
    #     print word


