import requests
from lxml import etree
import pymongo
import time
import re

headers = {"User-Agent": "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)"}
conn = pymongo.MongoClient("localhost", 27017)
db = conn["qs_db"]
myset = db["qs_duanzi"]
base_url = 'https://www.qiushibaike.com/text/page/'

for page in range(1, 21):
	url = base_url + str(page) + '/'
	print(url)
	response = requests.get(url, headers=headers)
	html = response.text
	duanzi = re.findall(r'<div class="article block untagged mb15.*?<img src="//(.*?)" alt=.*?<h2>(.*?)</h2>.*?<span>(.*?)</span>.*?<i class="number">(.*?)</i> 好笑</span>.*?<i class="number">(.*?)</i> 评论',html,re.S)
	print(len(duanzi))
	for i in range(0, len(duanzi)):
		user_icon_link, user_name, joke_content, like_num, comment_num = duanzi[i]
		print(user_icon_link, user_name, joke_content, like_num, comment_num)
		# 定义字典存mongo
		d = {
			"user_icon_link": user_icon_link,
			"user_name": user_name.strip(),
			"joke_content": joke_content.strip(),
			"like_num": like_num,
			"comment_num": comment_num
		}
		myset.insert_one(d)
	print('爬取第%s页完毕，将要休眠2秒钟后继续爬取'%page)
	time.sleep(2)