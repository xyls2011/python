# 导入队列包
import queue
# 导入线程包
import threading
# 导入json处理包
import json
# import pymongo
# 导入xpath处理包
from lxml import etree
# 导入请求处理包
import requests

class ThreadCrawl(threading.Thread):
    '''
    定义爬取网页处理类，从页码队列中取出页面，拼接url，请求数据，并把数据存到数据队列中
    '''
    def __init__(self, threadName, pageQueue, dataQueue):
        '''
        构造函数
        :param threadName:当前线程名称
        :param pageQueue: 页面队列
        :param dataQueue: 数据队列
        '''
        super(ThreadCrawl, self).__init__()
        self.threadName = threadName
        self.pageQueue = pageQueue
        self.dataQueue = dataQueue
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36"}

    def run(self):
        '''
        线程执行的run方法
        :return:
        '''
        while not self.pageQueue.empty():
            try:
                pageNum = self.pageQueue.get(False)
                url = "http://www.dfenqi.cn/Product/Category?category=4945805937081335060-0-0&pageIndex=" + str(pageNum)
                content = requests.get(url,headers = self.headers).text
                self.dataQueue.put(content)
                print(self.threadName + '爬取数据')
            except:
                pass

# 解析线程是否结束的标识
PARSE_THREAD_EXIST = False

class ParseThread(threading.Thread):
    '''
    网页数据解析类
    '''
    def __init__(self,threadName,dataQueue,fileName):
        '''
        解析线程的构造函数
        :param threadName:当前线程名称
        :param dataQueue:数据队列
        :param fileName:文件名
        '''
        super(ParseThread,self).__init__()
        self.threadName = threadName
        self.dataQueue = dataQueue
        self.fileName = fileName

    def run(self):
        '''
        解析线程的执行run方法，从数据队列取出数据，解析数据，再存入到本地文件中
        :return:
        '''
        while not PARSE_THREAD_EXIST:
            try:
                html = self.dataQueue.get(False)
                print(self.threadName + '取到数据')
                text = etree.HTML(html)
                # 解析网页中的数据，此处可根据需要，定制解析方法或解析类来实现
                titleList = text.xpath("//div[@class='liebiao']/ul/li/a/p/text()")
                with open(self.fileName,'a',encoding='utf-8') as f:
                    for title in titleList:
                        f.write(title + "\n")
                print(self.threadName + '解析完成')
            except:
                pass

def main():
    '''
    调度方法，main入口执行方法
    :return:
    '''
    # 创建页码队列，用于存储页码
    pageQueue = queue.Queue(50)
    for i in range(1, 51):
        pageQueue.put(i)
    # 数据队列，用于存储爬取的数据供解析线程使用
    dataQueue = queue.Queue()
    # 将解析结果保存的文件名
    fileName = 'file.txt'
    # 爬取线程的名称列表
    cawlThreadNameList = ['线程一', '线程二']
    crawThreadlList = []
    for threadName in cawlThreadNameList:
        thread = ThreadCrawl(threadName, pageQueue, dataQueue)
        thread.start()
        crawThreadlList.append(thread)

    # 解析线程的名称列表
    parseThreadNameList = ['解析线程一','解析线程二']
    parseThreadList = []
    for threadName in parseThreadNameList:
        thread = ParseThread(threadName,dataQueue,fileName)
        thread.start()
        parseThreadList.append(thread)
    # 等待爬取线程处理结束
    for thread in crawThreadlList:
        thread.join()
    # 判断数据队列中是否处理完成了，当处理完成后，将退出解析线程标识为True
    if pageQueue.empty():
        global PARSE_THREAD_EXIST
        PARSE_THREAD_EXIST = True
    # 等待解析线程退出
    for thread in parseThreadList:
        thread.join()


if __name__ == "__main__":
    main()