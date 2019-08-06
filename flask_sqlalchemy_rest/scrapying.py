from bs4 import BeautifulSoup
import requests
import json
from result_model import SearchResult, dbResult
from datetime import date


def scrape(url, title, description, sourceName):
    if ((url != "www.autoblog.comhttps") == True):
        dbResult.create_all()
        l = {}
        base_url = url
        # print(base_url)

        # Request URL and Beautiful Parser
        r = requests.get(base_url)
        soup = BeautifulSoup(r.text, "html.parser")
        product_title = soup.find("h1")
        product_content = soup.find_all("p")
        # p_content = BeautifulSoup(product_content, "html.parser").find("p")
        content_string = ''
        for item in product_content:
            content = item.text.replace('\n', "").replace('\t', "").replace('\xa0', "")
            content_string += content
        today = date.today()
        search = SearchResult(url, content_string, title, today, description, sourceName, 0.0)
        dbResult.session.add(search)
        dbResult.session.commit()
        l['content'] = content_string
        return json.dumps(l)


if __name__ == "__main__":
    print(scrape())
