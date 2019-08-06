from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

dbResult = SQLAlchemy()
ma = Marshmallow()


# Search Result Class/Model
class SearchResult(dbResult.Model):
    id = dbResult.Column(dbResult.Integer, primary_key=True)
    url = dbResult.Column(dbResult.String(100))
    content = dbResult.Column(dbResult.String())
    title = dbResult.Column(dbResult.String(500))
    datePublish = dbResult.Column(dbResult.DateTime)
    description = dbResult.Column(dbResult.String(300))
    sourceName = dbResult.Column(dbResult.String(300))
    score = dbResult.Column(dbResult.FLOAT)

    def __init__(self, url, content, title, datePublish, description, sourceName, score):
        self.url = url
        self.title = title
        self.content = content
        self.datePublish = datePublish
        self.description = description
        self.sourceName = sourceName
        self.score = score

# Search Result Schema
class SearchSchema(ma.Schema):
    class Meta:
        fields = ('id', 'url','content', 'title' , 'datePublish', 'description', 'sourceName', 'score')


# Init schema
search_schema = SearchSchema(strict=True)
search_schema = SearchSchema(many=True, strict=True)  # deal with multiple search Engine
