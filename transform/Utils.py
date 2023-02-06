import csv
import os

def try_except(func):
    def wrapper(*args, **kwargs):
        try:
            data = func(*args, **kwargs)
        except:
            data = None
        return data
    return wrapper

@try_except
def get_h1(soup):
    return soup.h1.string

@try_except
def get_sku(soup):
    return soup.find('span', attrs={'id': 'productNmId'}).get_text()

@try_except
def get_stars(soup):
    return soup.find('div', attrs={'class': 'product-page__common-info'}).find('span', attrs={'data-link': 'text{: product^star}'}).get_text()

@try_except
def get_price(soup):
    return soup.find('ins', attrs={'class': 'price-block__final-price'}).get_text()

@try_except
def get_original_price(soup):
    return soup.find('del', attrs={'class': 'price-block__old-price j-final-saving j-wba-card-item-show'}).get_text()

@try_except
def get_description(soup):
    return soup.find('p', attrs={'class': 'collapsable__text'}).get_text()

@try_except
def get_brand(soup):
    return soup.find('div', attrs={'class': 'product-page__brand-logo hide-mobile'}).find('a').get('title')

@try_except
def get_tables_specifications(soup):
    return soup.find('div', attrs={'class': 'collapsable__content j-add-info-section'}).find_all('table')

def prepare_specifications(tables):
    data_spec_all = {}
    data_spec = []
    for table in tables:
        caption = table.find('caption').get_text()
        for tr in table.find_all('tr'):
            char = tr.find('th').get_text()
            value = tr.find('td').get_text()
            data_spec.append([char.strip(), value.strip()])
        data_spec_all[caption] = data_spec

    return data_spec_all


def write_to_csv(data):
    filename = 'wildberries_data.csv'

    if not os.path.isfile(filename):
        with open(filename, "a", newline="") as file:
            columns = data.keys()
            # writer = csv.DictWriter(file, fieldnames=columns)
            # writer.writerow(data)
            writer = csv.writer(file)
            writer.writerow(columns)
        # CsvHandler(filename).write_to_csv_semicolon(data)
    with open(filename, "a", newline="") as file:
        columns = data.keys()
        writer = csv.DictWriter(file, fieldnames=columns)
        writer.writerow(data)
    # else:
    #     CsvHandler(filename).create_headers_csv_semicolon(data)
    #     CsvHandler(filename).write_to_csv_semicolon(data)