from requests_html import HTMLSession
import re
from matplotlib import pyplot as plt

salary_element = '<p.*>(\d+)K-(\d+)K</p>'
salary = []
disabled_button_element = '<button.* disabled="disabled">下一页</button>'
disabled_button = None
p=1

while not disabled_button:
	print('crawling page ' + str(p))
	link = 'https://sou.zhaopin.com/?p=' + str(p) + '&jl=530&kw=爬虫工程师&kt=3'
	session = HTMLSession()
	page = session.get(link)
	page.html.render(sleep=3)

	salary += re.findall(salary_element,page.html.html)
	disabled_button = re.findall(disabled_button_element, page.html.html)
	p += 1
	if p >= 2:
		break
	session.close()
print(salary)

# 求出每家公司的平均薪资，比如 [12, 15] 的平均值为 13
salary = [(int(s[0]) + int(s[1])) / 2 for s in salary]
# 划定薪资范围，便于展示，你也可以尝试其它展示方案
low_salary, middle_salary, high_salary = [0, 0, 0]
for s in salary:
    if s <= 15:
        low_salary += 1
    elif s > 15 and s <= 30:
        middle_salary += 1
    else:
        high_salary += 1
# 调节图形大小，宽，高
plt.figure(figsize=(6, 9))
# 定义饼状图的标签，标签是列表
labels = ['Python salary < 15K', 'Python salary = 15K~30K', 'Python salary > 30K']
data = [low_salary, middle_salary, high_salary]
plt.pie(data, labels=labels)
# 设置x，y轴刻度一致，这样饼图才能是圆的
plt.axis('equal')
plt.legend()
plt.show()