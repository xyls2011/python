import ssl
import threading
import time
import urllib.request
from queue import Queue
from lxml import etree


count = 0
class myThread(threading.Thread):
    def __init__(self, url, q):
        super(myThread, self).__init__()
        self.q = q
        self.headers = {

            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36'

        }
        self.url = url

    def run(self):
        self.parse_html()

    def send_request(self, url):
        request = urllib.request.Request(url=url, headers=self.headers)
        # 我这里需要加上ssl认证
        ssl._create_default_https_context = ssl._create_unverified_context
        response = urllib.request.urlopen(request)

        html_response = response.read().decode('utf-8')

        return html_response

    def parse_html(self):
        resp = self.send_request(self.url)
        html = etree.HTML(resp)
        div_list = html.xpath("//div[@class='index_only']//div[@id='container']/div")
        for div in div_list:
            name = div.xpath(".//img/@alt")[0]
            src = div.xpath(".//img/@src2")[0]
            # print(src)
            # print(name)
            self.q.put(name + '\t' + src)
            global count
            count += 1


def main():
    q = Queue()
    base_url = 'http://sc.chinaz.com/tupian/renwutupian_'

    url_list = [base_url + str(num) + '.html' for num in range(2, 302)]
    # print(url_list)
    Thread_list = []
    # 创建并启动线程
    for url in url_list:
        p = myThread(url, q)
        p.start()
        Thread_list.append(p)
    # 让主线程等待子线程执行完成
    for i in Thread_list:
        i.join()
    # 打印队列里存入的信息
    while not q.empty():
        print(q.get())


if __name__ == "__main__":
    start = time.time()
    main()
    print('总共耗时：%s' % (time.time() - start))
    print('total count', count)


