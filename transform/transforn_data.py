# загрузить все файлы .csv формата из папки parser
# взять оттуда только столбец name, добавить столбец id, добавить столбец категория (из названия файла)
# смержить все таблицы в одну (посмотреть в шпаргалках по pandas как это сделать)
# сохранить это в файл products1.csv, чтобы уже потом с ним работать

# при дальнейшей работе с этим файлом обязательно делать shaffle!

import os
import pandas as pd
import requests
from sklearn.utils import shuffle
from bs4 import BeautifulSoup
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import csv
import os

# def try_except(func):
#     def wrapper(*args, **kwargs):
#         try:
#             data = func(*args, **kwargs)
#         except:
#             data = None
#         return data
#     return wrapper
# 
# @try_except
# def get_h1(soup):
#     return soup.h1.string
# 
# @try_except
# def get_sku(soup):
#     return soup.find('span', attrs={'id': 'productNmId'}).get_text()
# 
# @try_except
# def get_stars(soup):
#     return soup.find('div', attrs={'class': 'product-page__common-info'}).find('span', attrs={'data-link': 'text{: product^star}'}).get_text()
# 
# @try_except
# def get_price(soup):
#     return soup.find('ins', attrs={'class': 'price-block__final-price'}).get_text()
# 
# @try_except
# def get_original_price(soup):
#     return soup.find('del', attrs={'class': 'price-block__old-price j-final-saving j-wba-card-item-show'}).get_text()
# 
# @try_except
# def get_description(soup):
#     return soup.find('p', attrs={'class': 'collapsable__text'}).get_text()
# 
# @try_except
# def get_brand(soup):
#     return soup.find('div', attrs={'class': 'product-page__brand-logo hide-mobile'}).find('a').get('title')
# 
# @try_except
# def get_tables_specifications(soup):
#     return soup.find('div', attrs={'class': 'collapsable__content j-add-info-section'}).find_all('table')
# 
# def prepare_specifications(tables):
#     data_spec_all = {}
#     data_spec = []
#     for table in tables:
#         caption = table.find('caption').get_text()
#         for tr in table.find_all('tr'):
#             char = tr.find('th').get_text()
#             value = tr.find('td').get_text()
#             data_spec.append([char.strip(), value.strip()])
#         data_spec_all[caption] = data_spec
# 
#     return data_spec_all
# 
# 
# def write_to_csv(data):
#     filename = 'wildberries_data.csv'
# 
#     if not os.path.isfile(filename):
#         with open(filename, "a", newline="") as file:
#             columns = data.keys()
#             # writer = csv.DictWriter(file, fieldnames=columns)
#             # writer.writerow(data)
#             writer = csv.writer(file)
#             writer.writerow(columns)
#         # CsvHandler(filename).write_to_csv_semicolon(data)
#     with open(filename, "a", newline="") as file:
#         columns = data.keys()
#         writer = csv.DictWriter(file, fieldnames=columns)
#         writer.writerow(data)
#     # else:
#     #     CsvHandler(filename).create_headers_csv_semicolon(data)
#     #     CsvHandler(filename).write_to_csv_semicolon(data)
# 
# def get_data():
#     directory = '..\extract'
#     df = pd.DataFrame(columns=['id','item_name','category'])
#     for filename in os.listdir(directory):
#         # print(filename)
#         f = os.path.join(directory, filename)
#         # # checking if it is a file
#         if os.path.isfile(f) and "csv" in f:
#             print(filename)
#         data = pd.read_csv(f)
#         print(data["id"])
#         break
# 
# # def filter_data(df):
# def parse_data(html):
#     soup = BeautifulSoup(html, 'html.parser')
#     h1 = get_h1(soup)
#     sku = get_sku(soup)
#     stars = get_stars(soup)
#     price = get_price(soup)
#     original_price = get_original_price(soup)
#     description = get_description(soup)
#     brand = get_brand(soup)
# 
#     tables = get_tables_specifications(soup)
#     specifications = prepare_specifications(tables) if tables else None
# 
#     payload = {
#         'h1': h1,
#         'sku': sku,
#         'price': re.findall(r'[0-9]+', re.sub(r'\xa0', '', price))[0] if price else None,
#         'original_price': re.findall(r'[0-9]+', re.sub(u'\xa0', '', original_price))[0] if original_price else None,
#         'description': description,
#         'stars': stars,
#         'brand': brand,
#         'specifications': specifications,
#     }
#     print(payload)
# 
#     write_to_csv(payload)


def get_description(url):
    driver = webdriver.Chrome('chromedriver.exe')
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    desc = soup.find('p', attrs={'class': 'collapsable__text'}).get_text()
    driver.close()
    driver.quit()
    return desc


df = pd.read_csv("../data/products.csv")
# print(df['Ссылка'][0])
# response = requests.get(df['Ссылка'][0])
# print(response)
# 
# driver = webdriver.Chrome('chromedriver.exe')
# driver.get(df['Ссылка'][0])
# soup = BeautifulSoup(driver.page_source, 'html.parser')
# desc = soup.find('p', attrs={'class': 'collapsable__text'}).get_text()
# print(desc)
# driver.close()
df = df.rename(columns={"Ссылка":'url'})
# df_shuffle = shuffle(df)
df_cut = df.iloc[:20]
descs = []
with open("descs.txt","w",encoding='utf-8') as f:
    for item in df_cut['url']:
        desc = get_description(item)
        descs.append(desc)
        print(desc)
        f.write(desc + "\n")
df_cut['descriptions'] = descs
df_cut.to_csv("cat_products_with_description")

# df_shuffle_cut['descriptions'] = df_shuffle_cut['url'].apply(lambda x: get_description(x))
# df.to_csv("products_with_description")
# parse_data(response.content)
# TODO: попробовать получить описание с помощью парсинга html страницы по ссылке (ссылка есть в столбце ссылка)


