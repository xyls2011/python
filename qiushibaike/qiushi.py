import requests
from lxml import etree
import pymongo
import time


class QiushiSpider:
    def __init__(self):
        self.headers = {"User-Agent": "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)"}
        # 链接对象
        self.conn = pymongo.MongoClient("localhost", 27017)
        # 库对象
        self.db = self.conn["Qiushi_DB1"]
        # 集合对象
        self.myset = self.db["duanzi"]

    # 解析并写入数据库
    def parsePage(self, html):
        parseHtml = etree.HTML(html)
        # 基准XPath,每个段子对象
        baseList = parseHtml.xpath('//div[contains(@id,"qiushi_tag_")]')
        # for循环遍历每个段子对象,1个1个提取
        for base in baseList:
            # base : <element at ...>
            # 用户昵称
            username = base.xpath('./div/a/h2')
            if username:
                username = username[0].text
            else:
                username = "匿名用户"
            # 段子内容
            content = base.xpath('./a/div[@class="content"]/span/text()')
            content = "".join(content).strip()
            # 好笑数量
            laughNum = base.xpath('.//i[@class="number"]')[0].text
            # 评论数量
            commentsNum = base.xpath('.//i[@class="number"]')[1].text
            # 定义字典存mongo
            d = {
                "username": username.strip(),
                "content": content.strip(),
                "laughNum": laughNum,
                "commentsNum": commentsNum
            }
            self.myset.insert_one(d)

    # 获取页面
    def getPage(self, url):
        response = requests.get(url, headers=self.headers)
        # response.enconding = "utf-8"
        html = response.text
        self.parsePage(html)

    def workOn(self):
        for page in range(1, 21):
            url = 'https://www.qiushibaike.com/text/page/' + str(page)+'/'
            print('正在爬取url：', url)
            self.getPage(url)
            time.sleep(2)

if __name__ == "__main__":
    print("start crawling qiushibaike:")
    spider = QiushiSpider()
    spider.workOn()
