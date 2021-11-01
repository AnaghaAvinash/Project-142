#Importing Flask, jsonify and request into it from flask.
from flask import Flask, jsonify, request
import pandas as pd

#Importing the 3 lists from storage.py, output and get_recommendation() function
from storage import all_articles, liked_articles, not_liked_articles
from demographic_filtering import output
from content_filtering import get_recommendations

#Defining the Flask App
app = Flask(__name__)

#Creating a GET API to return the list of all articles
@app.route("/get-article")
def get_article():
    movie_data = {
        "url": all_articles[0][11],
        "title": all_articles[0][12],
        "text": all_articles[0][13],
        "lang": all_articles[0][14],
        "total_events": all_articles[0][15]
    }
    return jsonify({
        "data": movie_data,
        "status": "success"
    })

#Making required lists.
all_articles = []
liked_articles = []
not_liked_articles = []

#Importing 'articles.csv' and reading all the data.
with open("articles.csv") as f:
    reader = pd.read_csv(f)
    data = list(reader)
    all_articles = data[1:]


#Creating the first GET request to get the first article.
@app.route("/get-article")
def get_article():
    return jsonify({
        "data": all_articles[0],
        "status": "success"
    })

#Creating the second POST request to mark the article as liked. Returning the success response.
@app.route("/liked-article", methods=["POST"])
def liked_article():
    article = all_articles[0]
    liked_articles.append(article)
    all_articles.pop(0)
    return jsonify({
        "status": "success"
    }), 201


#Creating the third POST request to mark the article as not liked. Returning the success response.
@app.route("/unliked-article", methods=["POST"])
def unliked_article():
    article = all_articles[0]
    not_liked_articles.append(article)
    all_articles.pop(0)
    return jsonify({
        "status": "success"
    }), 201

#Creating a GET API to return the list of popular articles
@app.route("/popular-articles")
def popular_articles():
    article_data = []
    for article in output:
        _d = {
            "url": article[0],
            "title": article[1],
            "text": article[2],
            "lang": article[3],
            "total_events": article[4]
        }
        article_data.append(_d)
    return jsonify({
        "data": article_data,
        "status": "success"
    }), 200

#Creating another GET API to return the list of recommended articles
@app.route("/recommended-articles")
def recommended_articles():
    all_recommended = []
    for liked_article in liked_articles:
        output = get_recommendations(liked_article[4])
        for data in output:
            all_recommended.append(data)
    import itertools
    all_recommended.sort()
    all_recommended = list(all_recommended for all_recommended,_ in itertools.groupby(all_recommended))
    article_data = []
    for recommended in all_recommended:
        _d = {
            "url": recommended[0],
            "title": recommended[1],
            "text": recommended[2],
            "lang": recommended[3],
            "total_events": recommended[4]
        }
        article_data.append(_d)
    return jsonify({
        "data": article_data,
        "status": "success"
    }), 200

#Defining the Flask App
if __name__ == "__main__":
    app.run()