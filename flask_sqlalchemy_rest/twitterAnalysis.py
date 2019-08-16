import tweepy
import re

from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
from datetime import datetime, timedelta
from nltk.tokenize import WordPunctTokenizer


ACC_TOKEN = '1161562831785013248-uP38DYYIAmn7udOGErFhD8l566xTMj'
ACC_SECRET = 'Ehe1BluMAU2K1orNCjtFe5s4zpVwNzRPwG8AfaMyqPMDU'
CONS_KEY = 'Ep716dcsf5H4ZxAZQ3RVtjXCP'
CONS_SECRET = '1RmWPBInTVhgQMsCkx5VTz5hlvaO3flRgvge07RKaAQ0hxgIQV'


def authentication(cons_key, cons_secret, acc_token, acc_secret):
    print("we are authenticating")
    auth = tweepy.OAuthHandler(cons_key, cons_secret)
    auth.set_access_token(acc_token, acc_secret)
    api = tweepy.API(auth)
    return api


def search_tweets(keyword, total_tweets):
    print(keyword)
    today_datetime = datetime.today().now()
    yesterday_datetime = today_datetime - timedelta(days=1)
    today_date = today_datetime.strftime('%Y-%m-%d')
    yesterday_date = yesterday_datetime.strftime('%Y-%m-%d')
    api = authentication(CONS_KEY,CONS_SECRET,ACC_TOKEN,ACC_SECRET)
    search_result = tweepy.Cursor(api.search,
                                  q=keyword,
                                  since=yesterday_date,
                                  result_type='recent',
                                  lang='en').items(total_tweets)
    return search_result


def clean_tweets(tweet):
    print("we are cleaning tweet")
    user_removed = re.sub(r'@[A-Za-z0-9]+','',tweet.decode('utf-8'))
    link_removed = re.sub('https?://[A-Za-z0-9./]+','',user_removed)
    number_removed = re.sub('[^a-zA-Z]', ' ', link_removed)
    lower_case_tweet= number_removed.lower()
    tok = WordPunctTokenizer()
    words = tok.tokenize(lower_case_tweet)
    clean_tweet = (' '.join(words)).strip()
    return clean_tweet


def get_sentiment_score(tweet):
    print("we are calculate sentiment score")
    client = language.LanguageServiceClient()
    document = types\
               .Document(content=tweet,
                         type=enums.Document.Type.PLAIN_TEXT)
    sentiment_score = client\
                      .analyze_sentiment(document=document)\
                      .document_sentiment\
                      .score
    return sentiment_score


def analyze_tweets(keyword, total_tweets):
    score = 0
    tweets = search_tweets(keyword,total_tweets)
    for tweet in tweets:
        cleaned_tweet = clean_tweets(tweet.text.encode('utf-8'))
        sentiment_score = get_sentiment_score(cleaned_tweet)
        score += sentiment_score
        print('Tweet: {}'.format(cleaned_tweet))
        print('Score: {}\n'.format(sentiment_score))
    final_score = round((score / float(total_tweets)),2)
    return final_score


def printResearch(keyword):
    #final_score = analyze_tweets(keyword, 5)
    final_score = get_sentiment_score(keyword)
    if final_score <= -0.25:
        status = 'NEGATIVE | ❌'
    elif final_score <= 0.25:
        status = 'NEUTRAL | 🔶'
    else:
        status = 'POSITIVE | ✅'
    text = 'Average score for ' + keyword+ ' is ' + str(final_score) + ' | ' + status
    print(keyword + ': ' + text)


if __name__ == '__main__':
    print(printResearch())
