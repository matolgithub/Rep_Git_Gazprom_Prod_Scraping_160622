import math
import requests
from bs4 import BeautifulSoup as bs
from pprint import pprint
from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog
import pyttsx3


def speaker_text(text):
    tts = pyttsx3.init()
    voices = tts.getProperty('voices')
    tts.setProperty('voice', 'ru')
    tts.say(f'{text}')
    tts.runAndWait()
    return text

def main_form():
    window = Tk()
    window["bg"] = "black"
    window.title("Python - choice user form.")
    text_1 = "Нажмите кнопку!"
    text_2 = "Привет! Я Алла. Cестра Алисы и Маруси. Что будем делать?"
    input_label_ID = Label(text=text_1, fg='white', bg='black')
    input_label_ID.grid(row=1, column=1, padx=5, pady=10, sticky="w")

    def exit_form():
        window.quit()

    def get_gazprom_suppliers_run():
        text_3 = 'Начинается создание списка!'
        text_4 = 'Закройте это окно и подождите некоторое время!'
        speaker_text(text_3 + text_4)
        messagebox.showinfo(text_3, text_4)
        sup_list = get_gazprom_suppliers()
        text_5 = 'Список поставщиков "Газпрома"'
        text_6 = 'Получен!'
        speaker_text(text_5 + text_6)
        messagebox.showinfo(text_5, text_6)
        window.quit()
        wind = Tk()
        text = Text(wind)
        for sup in sup_list:
            text.insert(INSERT, f'{sup}\n')
            text.pack()
        wind.mainloop()
        wind.quit()

    def suppliers_file_run(filename='gazprom_suppliers_file.txt'):
        text_7 = 'Начинается копирование данных в файл!'
        text_8 = 'Закройте это окно и подождите некоторое время!'
        speaker_text(text_7 + text_8)
        messagebox.showinfo(text_7, text_8)
        suppliers_file()
        text_9 = 'Список поставщиков "Газпрома"'
        text_10 = f'Успешно записан в файл {filename}.'
        speaker_text(text_9 + text_10)
        messagebox.showinfo(text_9, text_10)
        text_11 = 'Форма диалога.'
        text_12 = "Продолжаем? - нажмите Да, Закончим - нажмите Нет."
        speaker_text(text_12)
        ask_form_1 = messagebox.askquestion(text_11, text_12)
        if ask_form_1 == 'no':
            window.quit()

    def supplier_verification_run():
        text_13 = 'Начинается создание списка поставщиков "Газпрома"!'
        text_14 = 'Закройте это окно и подождите некоторое время!'
        speaker_text(text_13 + text_14)
        messagebox.showinfo(text_13, text_14)
        supplier_verification()
        text_15 = 'Проверка поставщиков "Газпрома"'
        text_16 = 'Проведена и закончена!'
        speaker_text(text_15 + text_16)
        messagebox.showinfo(text_15, text_16)
        text_17 = 'Форма диалога.'
        text_18 = "Остаться в главном меню? - нажмите Да, Хватит уже - нажмите Нет."
        speaker_text(text_18)
        ask_form_2 = messagebox.askquestion(text_17, text_18)
        if ask_form_2 == 'no':
            window.quit()

    button_1 = Button(text="Получить список поставщиков 'Газпрома'", activebackground='red', highlightcolor='red', bg='blue', fg='white', command=get_gazprom_suppliers_run)
    button_2 = Button(text="Записать список поставщиков 'Газпрома' в файл", activebackground='red', highlightcolor='red', bg='blue', fg='white', command=suppliers_file_run)
    button_3 = Button(text="Проверка на вхождение в список 'Газпрома'", activebackground='red', highlightcolor='red', bg='blue', fg='white', command=supplier_verification_run)
    button_4 = Button(text="Закрыть форму", activebackground='red', highlightcolor='red', bg='blue', fg='white', command=exit_form)
    button_1.grid(row=3, column=1, padx=30, pady=20, sticky='nesw')
    button_2.grid(row=4, column=1, padx=30, pady=20, sticky='nesw')
    button_3.grid(row=5, column=1, padx=30, pady=20, sticky='nesw')
    button_4.grid(row=10, column=1, padx=10, pady=20, sticky="e")
    speaker_text(text_2 + text_1)

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
        res_get = requests.get(url, headers=HEADERS)
        soup = bs(res_get.text, 'html.parser')
        count_comp = int(soup.find(class_="b-content__wrapper").find(class_="btn-more").attrs['data-total'])
        count_pages = math.ceil(count_comp / 100)

        companies_list = []
        count_companies = 0
        for num_page in range(1, count_pages + 1):
            url=f'https://reestr-neftegaz.ru/companies/gazprom_mtp/?name=&page={num_page}&collapse=open'
            res_get = requests.get(url, headers=HEADERS)
            soup = bs(res_get.text, 'html.parser')
            companies = soup.find(class_='b-content__wrapper').find_all(class_='b-block-top__name')
            for company in companies:
                count_companies += 1
                name_company = company.text.strip()
                companies_list.append([name_company])
        return companies_list

def suppliers_file(filename='gazprom_suppliers_file.txt'):
    suppliers = get_gazprom_suppliers()
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(f'Всего {len(suppliers)} компаний.' + '\n')
        for supplier in suppliers:
            file.write((str(supplier)).replace('[', '').replace(']', '') + '\n')
    return suppliers

def supplier_verification():
    suppliers_list = get_gazprom_suppliers()
    verif_result_list = [[], []]
    while True:
        text_19 = 'Ввод названия компании'
        text_20 = 'Введите название поставщика, которого нужно проверить в списке поставщиков "Газпрома: "'
        speaker_text(text_20)
        sdft = simpledialog.askstring(text_19, text_20)
        if sdft.isdigit():
            text_21 = 'Ошибка!'
            text_22 = 'Вы ввели цифры, попробуйте снова!'
            speaker_text(text_21 + text_22)
            messagebox.showinfo(text_21, text_22)
        else:
            text_23 = 'Проверка!'
            text_24 = f'Вы ввели {sdft} сейчас проверим!'
            speaker_text(text_24)
            messagebox.showinfo(text_23, text_24)
            for supplier in suppliers_list:
                if sdft.lower() == str(supplier).strip().replace('[', '').replace(']', '').lower():
                    verif_result_list[0].append(supplier)
                elif sdft.lower() in str(supplier).strip().replace('[', '').replace(']', '').lower():
                    verif_result_list[1].append(supplier)
            break
    if verif_result_list[0] != []:
        text_25 = 'Результат проверки!'
        text_26 = f'Поставщик {sdft} есть в списке поставщиков "Газпрома"!'
        speaker_text(text_26)
        messagebox.showinfo(text_25, text_26)
    elif verif_result_list[0] == [] and verif_result_list[1] != []:
        text_27 = 'Результат проверки!'
        text_28 = f'Ваш Поставщик: {sdft}. А в списке поставщиков "Газпрома" есть: {verif_result_list[1]}'
        speaker_text(text_28)
        messagebox.showinfo(text_27, text_28)
    elif verif_result_list == [[], []]:
        text_29 = 'Результат проверки!'
        text_30 = f'Поставщика {sdft} нет в списке поставщиков "Газпрома"!'
        speaker_text(text_30)
        messagebox.showinfo(text_29, text_30)
    return verif_result_list


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
