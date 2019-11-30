from bs4 import BeautifulSoup
import datetime
import lxml
import os
import requests
import utils

def run_file():
    '''
    scrapes all of today's articles on https://blogs.fangraphs.com/
    '''
    print(f'Running {__name__}')
    # get the links to all the articles
    url = 'https://blogs.fangraphs.com/'
    response = requests.get(url)
    page = response.text
    soup = BeautifulSoup(page, "lxml")
    links = utils.get_links(soup)

    # if an article was written today, save it
    today_datetime = datetime.datetime.now().date()
    article_title_lst = []
    article_date_lst = []
    article_text_lst = []

    for link in links:
        response = requests.get(link)
        page = response.text
        soup = BeautifulSoup(page, "lxml")
        article_date = utils.get_article_date(soup)
        article_date_datetime = datetime.datetime.strptime(article_date,
            '%B %d, %Y').date()
        if today_datetime == article_date_datetime:
            article_title = utils.get_article_title(soup)
            article_text = utils.get_article_text(soup)
            article_title_lst.append(article_title)
            article_date_lst.append(article_date)
            article_text_lst.append(article_text)

    if not os.path.exists('/Users/eric/ds/fangraphs/text_files'):
        os.makedirs('/Users/eric/ds/fangraphs/text_files')

    title = f'articles_{today_datetime}'.replace('-', '_')

    with open(f'/Users/eric/ds/fangraphs/text_files/{title}.txt', 'wb') as f:
        for title, date, text in zip(article_title_lst, article_date_lst,
            article_text_lst):
            f.write(title.encode('utf-8'))
            f.write('\n'.encode('utf-8'))
            f.write(date.encode('utf-8'))
            f.write(text.encode('utf-8'))
            article_seperator = '\n' + '-' * 100 + '\n'
            f.write(article_seperator.encode('utf-8'))
            f.write(article_seperator.encode('utf-8'))
            f.write(article_seperator.encode('utf-8'))

if __name__=='__main__':
    run_file()
