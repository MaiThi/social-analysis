from flask import Flask, request, jsonify

import os, time
from flask_cors import CORS
from scrapying import scrape
from searchApp import BingWebSearch
import json
from result_model import SearchResult, dbResult
from newsapi import NewsApiClient
from textSentiment import TextAnalysis
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
json_data_list = []
json_data_do = {}
json_data_do['id'] = 1
json_data_do['language'] ='en'
json_data_do['text'] = "Hello world. This is some input text that I love."
json_data_list.append(json_data_do)

json_data_do1 = {}
json_data_do1['id'] = 2
json_data_do1['language'] ='en'
json_data_do1['text'] = "Today it is not rain"
json_data_list.append(json_data_do1)
api = NewsApiClient(api_key='d68980504f584e1ba4788eeb20bd3fbe')

#TO DO: edit to delete method, after integrate angular project
@app.route('/searched/deleteAll', methods=['GET'])
def deleteSearch():
    results = SearchResult.query.all()
    for re in results:
        dbResult.session.delete(re)
        dbResult.session.commit()
    #SearchResult.query().delete()
    results = SearchResult.query.all()
    print(results)
    return "abc"


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
    search_result = SearchResult.query.all()
    text_list = []
    text_list.append(search_result[0])
    text_list.append(search_result[1])
    print(text_list)
    tex = TextAnalysis(text_list)
    a = []
    for i in tex:
        j = json.loads(i)
        record = {}
        record['id'] = j['id']
        record['source'] = j['sourceName']
        record['title'] = j['title']
        record['score'] = j['score']
        print(j)
        a.append(record)
    return json.dumps(a)


@app.route('/twitterAnalysis/<keyword>', methods=['GET'])
def twitter(keyword):
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = (r"C:\Users\MAIH004\My Project-4f1de5feb39a.json")
    bq_client = Client()
    search_result = SearchResult.query.all()
    printResearch(search_result[38].content)
    return 'abc'

if __name__ == '__main__':
    app.run()
