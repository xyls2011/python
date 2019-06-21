import requests
from pyquery import PyQuery as pq

url = 'https://www.zhihu.com/explore'
myheaders = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) '
                           'Chrome/59.0.3071.115 Safari/537.36'}
html = requests.get(url, headers=myheaders).text
# print(html)
# print('='*50+'\n')
doc = pq(html)
items = doc('.explore-feed.feed-item').items()
for item in items:
    question = item.find('h2').text()
    author = item.find('.author-link-line').text()
    answer = pq(item.find('.content').html()).text()
    with open('test.txt', 'w') as file:
        file.write('\n'.join([question, author, answer]))
        file.write('\n'+'='*50+'\n')
