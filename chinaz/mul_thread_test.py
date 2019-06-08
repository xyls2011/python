import multiprocessing
import ssl
import time
import urllib.request
from queue import Queue

from lxml import etree


class ZhanzProcess(multiprocessing.Process):

    def __init__(self, url, q):
        super(ZhanzProcess, self).__init__()

        self.q = q
        self.url = url
        self.headers = {

            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36'

        }

    def run(self):
        self.parse_html()

    def send_request(self, url):
        request = urllib.request.Request(url=url, headers=self.headers)
        ssl._create_default_https_context = ssl._create_unverified_context
        response = urllib.request.urlopen(request)
        html_response = response.read().decode('utf-8')

        return html_response

    def parse_html(self):
        res = self.send_request(self.url)
        html = etree.HTML(res)
        div_list = html.xpath("//div[@class='index_only']//div[@id='container']/div")
        for div in div_list:
            name = div.xpath(".//img/@alt")[0]
            src = div.xpath(".//img/@src2")[0]
            print(name + '\t' + src)

            self.q.put(name + '\t' + src)


def main():
    q = Queue()
    base_url = 'http://sc.chinaz.com/tupian/renwutupian_'

    url_list = [base_url + str(num) + '.html' for num in range(2, 50)]
    # print(url_list)
    process_list = []
    for url in url_list:
        # print(url)
        p = ZhanzProcess(url, q)
        p.start()
        process_list.append(p)

    for i in process_list:
        i.join()

    while not q.empty():
        print(q.get())


if __name__ == "__main__":
    start = time.time()
    main()
    print('总共耗时：%s' % (time.time() - start))