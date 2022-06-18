import math
import requests as re
from bs4 import BeautifulSoup as bs
from pprint import pprint



def get_gazprom_suppliers(site_link='https://reestr-neftegaz.ru/', url='https://reestr-neftegaz.ru/companies/gazprom_mtp/'):
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
    count_comp = int(soup.find(class_="b-content__wrapper").find(class_="btn-more").attrs['data-total'])
    count_pages = math.ceil(count_comp / 100)
    
    companies_list = []
    count_companies = 0
    print('*' * 100, 'Данные по компаниям: ')
    for num_page in range(1, count_pages + 1):
        url=f'https://reestr-neftegaz.ru/companies/gazprom_mtp/?name=&page={num_page}&collapse=open'
        res_get = re.get(url, headers=HEADERS)
        soup = bs(res_get.text, 'html.parser')
        
        companies = soup.find(class_='b-content__wrapper').find_all(class_='b-block-top__name')
        for company in companies:
            count_companies += 1
            name_company = company.text.strip()
            print(count_companies, name_company)
            companies_list.append([count_companies, name_company])

    print('*' * 100, 'Список компаний: ')
    pprint(companies_list)
    print('Количество компаний:', len(companies_list))
    return companies_list


def get_url(production='установка конденсаторная укм 58-0,4-200-12,5 у3', add_words='купить'):
    req_text = production + ' ' + add_words
    url_req_text  = req_text.replace(' ', '+').replace(',', '%2C')
    url = f'https://yandex.ru/search/?text={url_req_text}&lr=6&src=suggest_Pers'
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
    items = soup.find(class_='main__center').find_all(class_='Path Organic-Path path organic__path')
    for item in items:
        link_item = item.find('a').attrs['href']
        pprint(link_item)

if __name__ == '__main__':
    get_gazprom_suppliers()
    # get_url()