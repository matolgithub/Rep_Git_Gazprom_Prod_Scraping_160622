import requests as re
from bs4 import BeautifulSoup as bs
from pprint import pprint



def get_html_page(site_link='https://reestr-neftegaz.ru/', url='https://reestr-neftegaz.ru/companies/gazprom_mtp/'):
    HEADERS = {
        'accept-language': 'ru-RU,ru;q=0.9',
        'cookie': 'yandexuid=7517158921651275583; i=BfXMTmCzHSgXtAltGVouXdmLDy62Y88MRkbxDsxkvQcwZY2ZxGj3YY/QmyMKfqCv6VnD5UtWB+PFH36oUnMsrd7yVQk=; yuidss=7517158921651275583; ymex=1970333463.yrts.1654973463',
        'sec-ch-ua': '"Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'script',
        'sec-fetch-mode': 'no-cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.115 Safari/537.36'
    }
    res_get = re.get(url, headers=HEADERS)
    soup = bs(res_get.text, 'html.parser')
    pprint(soup)
    return soup, url, site_link

def get_companies():
    soup, url, site_link = get_html_page()
    count_companies = 0
    companies = soup.find_all(class_='')
    companies_list = []
    print('*' * 150, 'Данные по компаниям: ')
    for company in companies:
        count_companies += 1
        date_publ = article.find(class_="tm-article-snippet__datetime-published").find('time').attrs['title']
        title = article.find(class_="tm-article-snippet__title tm-article-snippet__title_h2").text
        article_link = article.find(class_="tm-article-snippet__title-link").attrs['href']
        hub = article.find(class_="tm-article-snippet__hubs").text
        try:
            article_text = article.find(class_="article-formatted-body article-formatted-body article-formatted-body_version-2").text
        except AttributeError:
            article_text = article.find(class_="article-formatted-body article-formatted-body article-formatted-body_version-1").text
        clean_article_text = article_text.replace('\n\n', '').replace('\r\n', ''). replace('\n', '').replace('\xa0', '')
        print(f'Статья №{count_companies}: Дата/время: {date_publ} -- Заголовок: {title} -- Ссылка: {site_link}'
                  f'{article_link} -- Текст статьи: {clean_article_text} -- Хабы: {hub}')
        companies_list.append([count_companies, date_publ, title, site_link + article_link, clean_article_text, hub])
    return companies_list





if __name__ == '__main__':
    get_companies()