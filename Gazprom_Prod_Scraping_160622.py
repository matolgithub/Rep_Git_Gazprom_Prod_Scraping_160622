import math
import requests
from bs4 import BeautifulSoup as bs
from pprint import pprint
import datetime
from tkinter import *
from tkinter import messagebox
import PySimpleGUI as sg
import time
from tkinter import simpledialog


def main_form():
    window = Tk()
    window["bg"] = "black"
    window.title("Python - choice user form.")
    input_label_ID = Label(text="Нажмите на кнопку исходя из того, что вы намерены сделать!", fg='white', bg='black')
    input_label_ID.grid(row=1, column=1, padx=5, pady=10, sticky="w")

    def get_gazprom_suppliers_run():
        get_gazprom_suppliers()
        window.quit()

    def suppliers_file_run():
        suppliers_file()
        window.quit()

    def supplier_verification_run():
        supplier_verification()
        window.quit()
    
    button_1 = Button(text="Получить список поставщиков 'Газпрома'", activebackground='red', highlightcolor='red', bg='blue', fg='white', command=get_gazprom_suppliers_run)
    button_2 = Button(text="Записать список поставщиков 'Газпрома' в файл", activebackground='red', highlightcolor='red', bg='blue', fg='white', command=suppliers_file_run)
    button_3 = Button(text="Проверка на вхождение в список 'Газпрома'", activebackground='red', highlightcolor='red', bg='blue', fg='white', command=supplier_verification_run)
    button_4 = Button(text="Закрыть форму", activebackground='red', highlightcolor='red', bg='blue', fg='white', command=exit)
    button_1.grid(row=3, column=1, padx=10, pady=20)
    button_2.grid(row=4, column=1, padx=10, pady=20)
    button_3.grid(row=5, column=1, padx=10, pady=20)
    button_4.grid(row=7, column=1, padx=10, pady=20, sticky="e")

            
    window.mainloop()


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
        messagebox.showinfo('Начинается создание списка!', 'Закройте это окно и подождите некоторое время!')
        res_get = requests.get(url, headers=HEADERS)
        soup = bs(res_get.text, 'html.parser')
        count_comp = int(soup.find(class_="b-content__wrapper").find(class_="btn-more").attrs['data-total'])
        count_pages = math.ceil(count_comp / 100)
        
        companies_list = []
        count_companies = 0
        # print('*' * 100, 'Данные по компаниям: ')
        for num_page in range(1, count_pages + 1):
            url=f'https://reestr-neftegaz.ru/companies/gazprom_mtp/?name=&page={num_page}&collapse=open'
            res_get = requests.get(url, headers=HEADERS)
            soup = bs(res_get.text, 'html.parser')
            companies = soup.find(class_='b-content__wrapper').find_all(class_='b-block-top__name')
            for company in companies:
                count_companies += 1
                name_company = company.text.strip()
                # print(count_companies, name_company)
                companies_list.append([name_company])
        messagebox.showinfo('Список поставщиков "Газпрома"', 'Получен!')
        # print('*' * 100, 'Список компаний: ')
        # pprint(companies_list)
        # print('Количество компаний:', len(companies_list))
        return companies_list

def suppliers_file(filename='gazprom_suppliers_file.txt'):
    messagebox.showinfo('Начинается копирование данных в файл!', 'Закройте это окно и подождите некоторое время!')
    with open(filename, 'w', encoding='utf-8') as file:
        suppliers = get_gazprom_suppliers()
        file.write(f'Всего {len(suppliers)} компаний.' + '\n')
        for supplier in suppliers:
            file.write((str(supplier)).replace('[', '').replace(']', '') + '\n')
    messagebox.showinfo(f'Список поставщиков "Газпрома"', 'Успешно записан в файл {filename}.')
    # print(f"The file {filename} was created! {datetime.datetime.now()}")
    return suppliers

def supplier_verification():
    suppliers_list = get_gazprom_suppliers()
    while True:
        sdft = simpledialog.askstring('Ввод названия компании', 'Введите название поставщика, которого нужно проверить в списке поставщиков "Газпрома: "')
        if sdft.isdigit():
            messagebox.showinfo('Ошибка!', 'Вы ввели цифры, попробуйте снова!')
        elif sdft.isalpha():
            messagebox.showinfo('Проверка!', f'Вы ввели {sdft} сейчас проверим!')
            for supplier in suppliers_list:
                if sdft == supplier:
                    messagebox.showinfo('Результат проверки!', f'Поставщик {sdft} есть в списке поставщиков "Газпрома"!')
                elif sdft in supplier:
                    messagebox.showinfo('Результат проверки!', f'Ваш Поставщик: {sdft}. А в списке поставщиков "Газпрома" есть похожая компания {supplier}.')
            break
    return sdft


def get_suppliers_url(production='установка конденсаторная укм 58-0,4-200-12,5 у3', add_words='купить'):
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
    res_get = requests.get(url, headers=HEADERS)
    soup = bs(res_get.text, 'html.parser')
    items = soup.find(class_='main__center').find_all(class_='Path Organic-Path path organic__path')
    for item in items:
        link_item = item.find('a').attrs['href']
        pprint(link_item)


if __name__ == '__main__':
    main_form()