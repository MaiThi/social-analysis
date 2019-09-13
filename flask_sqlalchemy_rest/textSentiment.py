from monkeylearn import MonkeyLearn
import json
from result_model import SearchResult, dbResult
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
from sqlalchemy.ext.declarative import DeclarativeMeta

ACC_TOKEN = '1161562831785013248-uP38DYYIAmn7udOGErFhD8l566xTMj'
ACC_SECRET = 'Ehe1BluMAU2K1orNCjtFe5s4zpVwNzRPwG8AfaMyqPMDU'
CONS_KEY = 'Ep716dcsf5H4ZxAZQ3RVtjXCP'
CONS_SECRET = '1RmWPBInTVhgQMsCkx5VTz5hlvaO3flRgvge07RKaAQ0hxgIQV'


class AlchemyEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                data = obj.__getattribute__(field)
                try:
                    json.dumps(data) # this will fail on non-encodable values, like other classes
                    fields[field] = data
                except TypeError:
                    fields[field] = None
            # a json-encodable dict
            return fields

        return json.JSONEncoder.default(self, obj)


def TextAnalysis(resultSearch):
    list= []
    ml = MonkeyLearn('61940ca317956cfc593a3b0234afd2775f994e69')
    data = []
    for search in resultSearch:
        insideData = {}
        insideData["text"] = search.content
        insideData["external_id"] = str(search.id)
        data.append(insideData)
    model_id = 'cl_pi3C7JiL'
    result = ml.classifiers.classify(model_id, data)
    for reColumn in result.body:
        json_data = json.dumps(reColumn)
        print(json_data)
        a = json.loads(json_data)
        print(a)
        searchResult = SearchResult.query.get(int(a["external_id"]))
        print('search' + searchResult.title)
        searchResult.score = a["classifications"][0]["confidence"]
        list.append(json.dumps(searchResult, cls=AlchemyEncoder))
        dbResult.session.commit()
    return list


def rescaleNumber(oldValue):
    newValue = ((oldValue + 1) * (1 - 0))/2
    return newValue


def GetSentimentScore():
    print("we are calculate sentiment score")
    search_result = SearchResult.query.all()
    for search in search_result:
        client = language.LanguageServiceClient()
        document = types\
                   .Document(content=search.content,
                             type=enums.Document.Type.PLAIN_TEXT)
        sentiment_score = client\
                          .analyze_sentiment(document=document)\
                          .document_sentiment\
                          .score
        numberScale = rescaleNumber(sentiment_score)
        search.score = round(float(numberScale),3)
        dbResult.session.commit()
    return "done"


if __name__ == "__main__":
    print(GetSentimentScore())
