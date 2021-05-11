import os
import re
import ray
import json
import itertools
import datetime
import requests
import pandas as pd
from bs4 import BeautifulSoup
from newspaper import Article

def read_query():
    with open(os.path.join(os.environ['CONFIG_DIR'], 'query.json'), 'r') as f:
        query = json.load(f)
    return query


def get_date():
    korean_time = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=9)
    korean_time += datetime.timedelta(days=-1)
    date = korean_time.strftime('%Y%m%d')
    return date


def url_to_soup(url):
    headers={'User-Agent':'Chrome/57.0.2987.110'}
    req = requests.get(url, headers=headers)
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')
    return soup


def collect_meta(query, date, maxlen=100):
    query_url = f'https://search.naver.com/search.naver?where=news&query={query}&nso=p:from{date}to{date}'
    title, url = [], []
    idx = 1

    while True:
        page_url = query_url + f'&start={idx}'
        soup = url_to_soup(page_url)
        news_area = soup.select('div.news_area')
        if not news_area: break
            
        cnt = 0
        news_area = [news.select('a.news_tit') for news in news_area]
        for news in news_area:
            _title, _url = news[0].get('title'), news[0].get('href')
            if _url not in url:
                title.append(_title)
                url.append(_url)
                cnt += 1
        
        if cnt == 0 or len(url) > maxlen:
            title, url = title[:maxlen], url[:maxlen]
            break
        idx += 10
    
    meta = pd.DataFrame({'title':title, 'url':url})
    return meta


def collect_news(query_set, date):
    data = []
    for query in query_set:
        _data = collect_meta(query, date)
        data.append(_data)
    data = pd.concat(data, ignore_index=True)
    
    data['text'] = ray.get([collect_text.remote(url) for url in data['url']])
    data['text'] = ray.get([clean_text.remote(text) for text in data['text']])
    data = data.dropna()
    data = data.loc[data['text'].apply(len).between(100, 1000)]
    data = data.reset_index(drop=True)
    return data


@ray.remote
def collect_text(url):
    try:
        article = Article(url, language='ko')
        article.download()
        article.parse()
        if article: 
            return article.text
    except:
        pass
    return None


@ray.remote
def clean_text(text):
    if text:
        text = re.sub('[\t\r\f\v]', ' ', text)
        text = re.sub('\[[\w\W=]+\]', ' ', text)
        text = re.sub('[a-zA-Z0-9.]+@[a-zA-Z0-9.]+', '', text)
        text = re.sub('무단전재 및 재배포 금지', '', text)
        text = re.sub('(저작권자)* © [\w]+', '', text)

        text = text.split('\n')
        text = [i for i in text if len(i) > 1]
        text = [re.findall('[\w\W]+?[다음함임까]+[.?!]+', i) for i in text]
        text = list(itertools.chain(*text))
        text = [i.strip() for i in text]

        text = '\n\n'.join(text)
    return text



    # @ray.remote
# def clean_text(text):
#     if text:
#         text = re.sub('[^가-힇ㄱ-ㅎㅏ-ㅣa-zA-Z0-9\s.-\[\]\(\)\'\"@]', ' ', text)
#         text = re.findall('[\w\W]+?[다음함임까]+[.?!]+', text)
#         text = '\n\n'.join(text)
#         text = text.strip()
#     return text