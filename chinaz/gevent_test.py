import ssl
import time
import urllib.request
from queue import Queue

import gevent as gevent
from lxml import etree

# 打猴子补丁
from gevent import monkey

monkey.patch_all()


class Zzspider(object):

    def __init__(self):
        self.q = Queue()
        self.headers = {

            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36'

        }

    def run(self, url):
        self.parse_html(url)

    def send_request(self, url):
        request = urllib.request.Request(url=url, headers=self.headers)
        ssl._create_default_https_context = ssl._create_unverified_context
        response = urllib.request.urlopen(request)
        html_response = response.read().decode('utf-8')

        return html_response

    def parse_html(self, url):
        res = self.send_request(url)
        html = etree.HTML(res)
        div_list = html.xpath("//div[@class='index_only']//div[@id='container']/div")
        for div in div_list:
            name = div.xpath(".//img/@alt")[0]
            src = div.xpath(".//img/@src2")[0]

            self.q.put(name + '\t' + src)

    def main(self):
        base_url = 'http://sc.chinaz.com/tupian/renwutupian_'

        url_list = [base_url + str(num) + '.html' for num in range(2, 50)]
        job_list = [gevent.spawn(self.run, url) for url in url_list]
        # 让线程等待所有任务完成，再继续执行。
        gevent.joinall(job_list)
        while not self.q.empty():
            print(self.q.get())


if __name__ == '__main__':
    start = time.time()
    zz = Zzspider()
    zz.main()
    print('总共耗时：%s' % (time.time() - start))