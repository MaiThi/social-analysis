from flask import Flask, request, jsonify

import os, time
from flask_cors import CORS
from scrapying import scrape
from searchApp import BingWebSearch
import json
from result_model import SearchResult, dbResult
from twitter_result_model import TwitterSearchModel, dbTwitterResult
from newsapi import NewsApiClient
from textSentiment import GetSentimentScore
from twitterAnalysis import printResearch
import os
from google.cloud.bigquery.client import Client

#Init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
#Init database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
CORS(app)

dbResult.init_app(app)
dbTwitterResult.init_app(app)
api = NewsApiClient(api_key='d68980504f584e1ba4788eeb20bd3fbe')

#TO DO: edit to delete method, after integrate angular project
@app.route('/searched/deleteAll', methods=['GET'])
def deleteSearch():
    results = SearchResult.query.all()
    for re in results:
        dbResult.session.delete(re)
        dbResult.session.commit()
    #SearchResult.query().delete()
    resultsTwitter = TwitterSearchModel.query.all()
    for re in resultsTwitter:
        dbTwitterResult.session.delete(re)
        dbTwitterResult.session.commit()
    return "finish"


@app.route('/search/<keyword>', methods=['GET'])
def search_with_key_word(keyword):
    print(keyword)
    result = api.get_everything(q=keyword)
    #json_data = json.loads(result)
    for index in result["articles"]:
       scrape(index["url"], index["title"], index["description"], index["source"]["name"])
    results = SearchResult.query.all()
    for re in results:
        print(re)
    return json.dumps(result)
    #return json.dumps(json_data["value"][0])

@app.route('/analysic')
def text_analytic():
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = (r"C:\Users\MAIH004\My Project-4f1de5feb39a.json")
    bq_client = Client()
    #result = GetSentimentScore()
    text_list = SearchResult.query.all()
    a = []
    sum = 0;
    density = [0] *10
    print(density)
    for i in text_list:
        record = {}
        sum += i.score;
        if (i.score * 100) <= 10:
            density[0] += 1
        if ((i.score * 100) > 10) and ((i.score * 100) <= 20):
            density[1] += 1
        if ((i.score * 100) > 20) and ((i.score * 100) <= 30):
            density[2] += 1
        if ((i.score * 100) > 30) and ((i.score * 100) <= 40):
            density[3] += 1
        if ((i.score * 100) > 40) and ((i.score * 100) <= 50):
            density[4] += 1
        if ((i.score * 100) > 50) and ((i.score * 100) <= 60):
            density[5] += 1
        if ((i.score * 100) > 60) and ((i.score * 100) <= 70):
            density[6] += 1
        if ((i.score * 100) > 70) and ((i.score * 100) <= 80):
            density[7] += 1
        if ((i.score * 100) > 80) and ((i.score * 100) <= 90):
            density[8] += 1
        if ((i.score * 100) > 90) and ((i.score * 100) <= 100):
            density[9] += 1
        record['id'] = i.id
        record['source'] = i.sourceName
        record['title'] = i.title
        record['score'] = i.score
        record['content'] = i.content
        record['url'] = i.url
        record['description'] = i.description
        a.append(record)
    print(density)
    averageScore = round(float(sum / 20),2)
    JSONResult = {}
    JSONResult['average'] = averageScore
    JSONResult['list'] = a
    JSONResult['chartData'] = density
    return json.dumps(JSONResult)


@app.route('/get-twitters')
def show_twitters():
    search_result = TwitterSearchModel.query.all()
   # tex = TextAnalysis(text_list)
    a = []
    sum = 0;
    density = [0] * 10
    for i in search_result:
        record = {}
        sum += i.score;
        if (i.score * 100) <= 10:
            density[0] += 1
        if ((i.score * 100) > 10) and ((i.score * 100) <= 20):
            density[1] += 1
        if ((i.score * 100) > 20) and ((i.score * 100) <= 30):
            density[2] += 1
        if ((i.score * 100) > 30) and ((i.score * 100) <= 40):
            density[3] += 1
        if ((i.score * 100) > 40) and ((i.score * 100) <= 50):
            density[4] += 1
        if ((i.score * 100) > 50) and ((i.score * 100) <= 60):
            density[5] += 1
        if ((i.score * 100) > 60) and ((i.score * 100) <= 70):
            density[6] += 1
        if ((i.score * 100) > 70) and ((i.score * 100) <= 80):
            density[7] += 1
        if ((i.score * 100) > 80) and ((i.score * 100) <= 90):
            density[8] += 1
        if ((i.score * 100) > 90) and ((i.score * 100) <= 100):
            density[9] += 1
        record['id'] = i.id
        record['tweet'] = i.tweet
        record['score'] = i.score
        print(i)
        a.append(record)
    averageScore = round(float(sum / 20), 3)
    JSONResult = {}
    JSONResult['averageTwitter'] = averageScore
    JSONResult['listTwitter'] = a
    JSONResult['chartDataTwitter'] = density
    return json.dumps(JSONResult)


@app.route('/twitterAnalysis/<keyword>', methods=['GET'])
def twitter(keyword):
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = (r"C:\Users\MAIH004\My Project-4f1de5feb39a.json")
    bq_client = Client()
    #search_result = SearchResult.query.all()
    printResearch(keyword)
    return json.dumps('abc')


@app.route('/dash-board')
def show_dashboard():
    search_result = SearchResult.query.all()
    text_list = []
    text_list.append(search_result[0])
    text_list.append(search_result[1])
   #tex = TextAnalysis(text_list)
    a = []
    for i in text_list:
        record = {}
        record['id'] = i.id
        record['source'] = i.sourceName
        record['title'] = i.title
        record['score'] = i.score
        record['content'] = i.content
        record['url'] = i.url
        record['description'] = i.description
        print(i)
        a.append(record)
    return json.dumps(a)


if __name__ == '__main__':
    app.run()
