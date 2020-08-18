import pandas as pd
import requests
from bs4 import BeautifulSoup


def get_soup(url, session):
    request = session.get(url)
    soup = BeautifulSoup(request.text, features='lxml')
    return soup


def parse_catalog_page(page, session):
    url = f'https://gazoncity.ru/catalog/?PAGEN_1={page}'
    soup = get_soup(url, session)
    goods_list = soup.find(
        'div', {'class': 'catalog item-views list image-top'})
    items = goods_list.find_all('div', {'class': 'item'})
    next_page = soup.find('li', {'class': 'next'})
    links_list = []
    for item in items:
        item_link = item.find('div', class_='title').find('a').get('href')
        links_list.append(item_link)
    return links_list, next_page


def parse_item_page(session, url):
    result = []
    site_url = 'https://gazoncity.ru'
    item_url = site_url + url
    soup = get_soup(item_url, session)
    name = soup.find('h1', id='pagetitle').text
    price = soup.find('span', class_='price_val').text
    price = price.replace(' ', '')
    img_link = soup.find('img', itemprop='image').get('src')
    description = soup.find('div', class_='previewtext').text
    result.append({'Название': name,
                   'Цена, р.': float(price[:-2]),
                   'URL-картинки': site_url + img_link,
                   'Описание': description})
    return result


def get_goods_links(session, page=1):
    links_list = []
    while True:
        links, next_page = parse_catalog_page(page, session)
        links_list.extend(links)
        if next_page:
            page += 1
        else:
            return links_list


def get_goods_information(session):
    links_list = get_goods_links(s)
    result = []
    for item in links_list:
        result.extend(parse_item_page(session, item))
    return result


if __name__ == "__main__":
    s = requests.Session()
    result = get_goods_information(s)
    data_df = pd.DataFrame(result)
    data_df.to_excel('gazoncity.xlsx')
