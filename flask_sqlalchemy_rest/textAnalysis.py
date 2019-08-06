import http.client
import urllib.parse
import json, requests
from pprint import pprint

subscriptionKey = "27f0eb50ff1f4428bdc83a7cdd8dbab5"

# Verify the endpoint URI.  At this writing, only one endpoint is used for Bing
# search APIs.  In the future, regional endpoints may be available.  If you
# encounter unexpected authorization errors, double-check this value against
# the endpoint for your Bing Web search instance in your Azure dashboard.
host = "api.cognitive.microsoft.com"
path = "/text/analytics/v2.0/sentiment"
SENTIMENT_URL = "https://westeurope.api.cognitive.microsoft.com/text/analytics/v2.1/"
sentiment_url = SENTIMENT_URL + "sentiment"


def TextAnalysis(documents):
    documents = {"documents": documents}
    print(documents)
    headers = {"Ocp-Apim-Subscription-Key": subscriptionKey}
    response = requests.post(sentiment_url, headers=headers, json=documents)
    sentiments = response.json()
    return sentiments


if __name__ == "__main__":
    print(TextAnalysis())
