#!/usr/bin/env python
# encoding=utf-8
#https://gist.github.com/lijsh/2a0b3991cf7d15ae144a
#https://zhuanlan.zhihu.com/p/20423182

"""
爬取豆瓣图书TOP250 - 完整示例代码
"""

import codecs

import requests
from bs4 import BeautifulSoup

DOWNLOAD_URL = 'http://book.douban.com/top250/'


def download_page(url):
    return requests.get(url, headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'
    }).content


def parse_html(html):
    soup = BeautifulSoup(html)
    book_list_soup = soup.find('div', attrs={'class': 'indent'})

    book_name_list = []

    for book_li in book_list_soup.find_all('table'):
        book_img = book_li.find('img').get('src')
        print('book_img',book_img)
        detail = book_li.find('div', attrs={'class': 'pl2'})
        book_name = detail.find('a').getText(strip=True)

        print(book_name)

        book_name_list.append(book_name)

    next_page = soup.find('span', attrs={'class': 'next'}).find('a')
    if next_page:
        return book_name_list, next_page['href']
    return book_name_list, None


def main():
    url = DOWNLOAD_URL

    with codecs.open('books', 'wb', encoding='utf-8') as fp:
        while url:
            html = download_page(url)
            books, url = parse_html(html)
            fp.write(u'{books}\n'.format(books='\n'.join(books)))


if __name__ == '__main__':
    main()
