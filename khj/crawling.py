import requests
from bs4 import BeautifulSoup
import pandas as pd

# 요청 헤더 추가
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"}


def get_news(query):
    news_df = pd.DataFrame(columns=("press", "title", "category", "article", "datetime", "link"))
    news_dfs = pd.DataFrame(columns=("press", "title", "article"))
    idx = 0

    url = requests.get(f'https://search.naver.com/search.naver?where=news&sm=tab_jum&query={query}',
                       headers=headers).content
    soup = BeautifulSoup(url, 'html.parser')
    linkss = soup.find_all('div', class_='info_group')

    for links in linkss:
        news_urls = links.select('a:nth-of-type(2)')
        for news_url in news_urls:
            link = news_url.get('href')
            if link == '#':
                continue
            else:
                news_link = requests.get(link, headers=headers)
                news_html = BeautifulSoup(news_link.text, 'html.parser')
                try:
                    press = news_html.find('img').get('title')
                    if press:
                        press = press.replace('"', '')
                        press = press.replace("'", "")

                        title = news_html.find('h2', id='title_area').get_text()
                        title = title.replace('"', '')
                        title = title.replace("'", "")

                        datetime = news_html.find('span',
                                                  class_='media_end_head_info_datestamp_time _ARTICLE_DATE_TIME').get_text()
                        datetime = datetime.replace('"', '')
                        datetime = datetime.replace("'", "")

                        article = news_html.find('div', id='dic_area').get_text()
                        article = article.replace('\n', '')
                        article = article.replace('\t', '')
                        article = article.replace('"', '')
                        article = article.replace("'", "")

                        category = news_html.find('em', class_='media_end_categorize_item').get_text()

                        news_df.loc[idx] = [press, title, category, article, datetime, link]
                        return news_df
                    else:
                        press = news_html.find('p', class_='source').get_text()
                        press = press.replace('기사제공 ', '')
                        title = news_html.find('h4', class_='title').get_text()
                        article = news_html.find('div', id='newsEndContents').get_text().replace('\t', '').replace('\n',
                                                                                                                   '')
                        em_tag = news_html.find('em', class_='img_desc').get_text()
                        p_tag = news_html.find('p', class_='byline').get_text()
                        p_tag1 = news_html.find('p', class_='source').get_text()
                        div_tag = news_html.find('div', class_='article_notice_txt').get_text()
                        div_tag1 = news_html.find('div', class_='subscribe_layer').get_text()
                        article = article.replace(em_tag, '').replace(p_tag, '').replace(div_tag, '').replace(p_tag1, '').replace(div_tag1, '')
                        news_dfs.loc[idx] = [press, title, article]
                        return news_dfs
                except:
                    continue

