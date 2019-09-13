from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

dbTwitterResult = SQLAlchemy()
ma = Marshmallow()


# Twitter Search Result Class/Model
class TwitterSearchModel(dbTwitterResult.Model):
    id = dbTwitterResult.Column(dbTwitterResult.Integer, primary_key=True)
    tweet = dbTwitterResult.Column(dbTwitterResult.String(1000))
    score = dbTwitterResult.Column(dbTwitterResult.FLOAT)

    def __init__(self, tweet, score):
        self.tweet = tweet
        self.score = score


# Search Result Schema
class TwitterSearchSchema(ma.Schema):
    class Meta:
        fields = ('id', 'tweet', 'score')


# Init schema
twitter_schema = TwitterSearchSchema(strict=True)
twitter_schema = TwitterSearchSchema(many=True, strict=True)  # deal with multiple search Engine
