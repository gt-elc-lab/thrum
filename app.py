from flask import Flask, json, render_template, request, jsonify
from collection.models import Post
from analysis.tfidf import TFIDF
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

if __name__ == "__main__":
    app.run(debug=True)