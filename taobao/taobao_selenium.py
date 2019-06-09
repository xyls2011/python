import pymongo
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from pyquery import PyQuery as pq
# from config import *
from urllib.parse import quote

# 无界面模式
chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--headless')
browser = webdriver.Chrome(chrome_options=chrome_options)
# 浏览器需要多次使用，所以单独拿出来。设置一个最长的等待时间,等待目标加载完成
wait = WebDriverWait(browser, 10)
KEYWORD = 'coser'
MONGO_URL = 'localhost'
MONGO_DB = 'TAOBAO_COSER'
MONGO_COLLECTION = 'products'
client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]
MAX_PAGE = 38


def index_page(page):
    """
    抓取索引页
    :param page: 页码
    """
    print('正在爬取第', page, '页')
    # wait容易出现加载时间长的问题，因此用try来捕捉异常
    try:
        url = 'https://s.taobao.com/search?q=' + quote(KEYWORD)
        browser.get(url)
        # 加载需要一定时间的，设置了等待时间，等待加载
        # 输入按钮的加载等待
        # 首先访问搜索商品的链接，然后判断当前的页码，如果大于1，就进行跳页操作，否则等待加载完成
        if page > 1:
            # 输入按钮的加载等待
            input = wait.until(
                # 设置加载目标，它是一个选择器，参数是需要选择方式和等待加载的内容
                # ‘>’意味选择所有父级id='mainsrp-pager div form'的id='input'的元素
                # 表示CSS的空格用.
                EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-pager div.form > input')))
            # 提交按钮  ,先通过上一步填页码，再通过这一步提交
            submit = wait.until(
                # EC后面是选择条件，按钮的加载条件最好的是element_to_be_clickable，意思为元素可以点击的
                EC.element_to_be_clickable((By.CSS_SELECTOR, '#mainsrp-pager div.form > span.btn.J_Submit')))
            input.clear()
            input.send_keys(page)  # 对输入框输入内容
            submit.click()  # 提交搜索内容，进入下一页面
        wait.until(
            # 若当前跳转的页码是高亮状态
            EC.text_to_be_present_in_element((By.CSS_SELECTOR, '#mainsrp-pager li.item.active > span'), str(page)))
        # 等待页码元素加载完成
        # '.m-itemlist .items .item'这个选择器对应的每个商品的信息块
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.m-itemlist .items .item')))
        get_products()  # 等待加载完成后，提取商品信息
    except TimeoutException:
        # 超时后重新请求，因此递归调用
        index_page(page)


def get_products():
    """
    提取商品数据
    """
    html = browser.page_source  # 获取网页源码
    doc = pq(html)
    print('getting product...')
    # 匹配整个页面的每个商品，然后进行遍历
    items = doc('#mainsrp-itemlist .items .item').items()
    for item in items:
        product = {
            'image': item.find('.pic .img').attr('data-src'),  # 返回元素属性值
            'price': item.find('.price').text(),
            'deal': item.find('.deal-cnt').text(),
            'title': item.find('.title').text(),
            'shop': item.find('.shop').text(),
            'location': item.find('.location').text()
        }
        print(product)
        save_to_mongo(product)


# 此处的result变量是get_products()方法传过来的product，包含单个商品的信息
def save_to_mongo(result):
    """
    保存至MongoDB
    :param result: 结果
    """
    try:
        if db[MONGO_COLLECTION].insert(result):
            print('存储到MongoDB成功')
    except Exception:
        print('存储到MongoDB失败')


def main():
    """
    遍历每一页
    """
    for i in range(1, MAX_PAGE + 1):
        index_page(i)
    browser.close()


if __name__ == '__main__':
    main()