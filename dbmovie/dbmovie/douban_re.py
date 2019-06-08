import requests
import re
url = 'https://movie.douban.com/top250'
#访问网站，并获得回复和网页原代码
response = requests.get(url)
response.encoding = 'utf-8'
html = response.text
title = re.findall(r'<h1>(.*?)</h1>',html)[0]
#打开文本文件，并以‘title’为文件名
fb = open('%s.txt' % title, 'w', encoding='utf-8')
#用正则表达式来获得当前页面的排名
ranks = re.findall(r'<em class="">(.*?)</em>.*?<a href="(.*?)">.*?<img width="100" alt="(.*?)" src="(.*?)" class="">',html,re.S)
#用正则表达式来获得当前页面的分数
points = re.findall(r'<span class="rating_num" property="v:average">(.*?)</span>.*?<span>(.*?)</span>',html,re.S)
#用正则表达式来获得后面排名的网页链接
next_list = re.findall(r'<span class="thispage">1</span>(.*?)<span class="next">',html,re.S)[0]
print(next_list)
next_list = re.findall(r'<a href="(.*?)" >.*?</a>',next_list,re.S)
print(next_list)
# 先处理1—25名的数据
for i in range(0, 25):
    number, movie, name, picture = ranks[i]
    score, people = points[i]
    fb.write(number + '  ' + name)
    fb.write('\n')
    fb.write('电影链接：' + movie)
    fb.write('\n')
    fb.write('电影海报链接：' + picture)
    fb.write('\n')
    fb.write(people + '为：' + score + '分' + '\n')
#处理剩余排名的数据
for next in next_list:
    #把获得的链接补全，便于正常访问
    next = "https://movie.douban.com/top250%s" % next
    #获得剩余排名的电影的数据
    next_response = requests.get(next)
    # next_response.encoding = 'utf-8'
    next_html = next_response.text
    ranks = re.findall(r'<em class="">(.*?)</em>.*?<a href="(.*?)">.*?<img width="100" alt="(.*?)" src="(.*?)" class="">', next_html, re.S)
    points = re.findall(r'<span class="rating_num" property="v:average">(.*?)</span>.*?<span>(.*?)</span>', next_html, re.S)
    for i in range(0,25):
        number, movie, name, picture = ranks[i]
        score, people = points[i]
        fb.write(number + '  ' + name)
        fb.write('\n')
        fb.write('电影链接：' + movie)
        fb.write('\n')
        fb.write('电影海报链接：' + picture)
        fb.write('\n')
        fb.write(people + '为：' + score + '分' + '\n')
#完成访问后关闭文本文件和访问请求
fb.close()
response.close()