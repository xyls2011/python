import requests
from urllib.parse import urlencode
from requests import codes
import os
from hashlib import md5
from multiprocessing.pool import Pool
import re


myheaders = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) '
                           'Chrome/59.0.3071.115 Safari/537.36'}
def get_page(offset):
    params = {
        'aid': '24',
        'offset': offset,
        'format': 'json',
        #'keyword': '街拍',
        'autoload': 'true',
        'count': '20',
        'cur_tab': '1',
        'from': 'search_tab',
        'pd': 'synthesis'
    }
    base_url = 'https://www.toutiao.com/api/search/content/?keyword=%E8%A1%97%E6%8B%8D'
    url = base_url + urlencode(params)
    try:
        resp = requests.get(url, headers=myheaders)
        print('test url: ', url)
        if 200 == resp.status_code:
            print('resp.status_code1 ', resp.status_code)
            # print(resp.json())
            return resp.json()
    except requests.ConnectionError:
        return None


def get_images(json):
    if json.get('data'):
        data = json.get('data')
        for item in data:
            if item.get('cell_type') is not None:
                continue
            title = item.get('title')
            images = item.get('image_list')
            for image in images:
                # origin_image = re.sub("list", "origin", image.get('url'))
                origin_image = image.get('url')
                yield {
                    'image':  origin_image,
                    # 'iamge': image.get('url'),
                    'title': title
                }

print('succ')

def save_image(item):
    img_path = 'img' + os.path.sep + item.get('title')
    print('succ2')
    if not os.path.exists(img_path):
        os.makedirs(img_path)
    try:
        print('item.get_image_url ', item.get('image'))
        resp = requests.get(item.get('image'), headers=myheaders)
        print('resp.status_code2 ', resp.status_code)
        if codes.ok == resp.status_code:
            file_path = img_path + os.path.sep + '{file_name}.{file_suffix}'.format(
                file_name=md5(resp.content).hexdigest(),
                file_suffix='jpg')
            if not os.path.exists(file_path):
                print('succ3')
                with open(file_path, 'wb') as f:
                    f.write(resp.content)
                print('Downloaded image path is %s' % file_path)
                print('succ4')
            else:
                print('Already Downloaded', file_path)
    except requests.ConnectionError:
        print('Failed to Save Image，item %s' % item)


def main(offset):
    json = get_page(offset)
    for item in get_images(json):
        print('main item: ', item)
        save_image(item)


GROUP_START = 0
GROUP_END = 1

if __name__ == '__main__':
    pool = Pool()
    groups = ([x * 20 for x in range(GROUP_START, GROUP_END + 1)])
    pool.map(main, groups)
    pool.close()
    pool.join()
