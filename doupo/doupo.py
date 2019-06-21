import re
import requests
import time

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'}

f = open('doupoxs.txt','a+')

def get_txt(url):
	res = requests.get(url,headers=headers)
	print(res.status_code)
	if res.status_code == 200:
		print('page found',url)
		contents = re.findall('<p>(.*?)</p>',res.content.decode('utf-8'),re.S)
		for content in contents:
			print(content)
			f.write(content + '\n')
	else:
		print('page not found...')

if __name__ == '__main__':
	urls = ['http://www.doupoxs.com/doupocangqiong/{}.html'.format(num) for num in range(1,20)]
	for url in urls:
		print(url)
		get_txt(url)
		time.sleep(1)
	f.close()