import random
import time

import bs4
import requests

for page in range(1, 11):
    resp = requests.get(
        url=f'https://movie.douban.com/top250?start={(page - 1) * 25}',
        # 通过设置请求头将爬虫程序伪装为浏览器
        headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                          ' AppleWebKit/537.36 (KHTML, like Gecko)'
                          ' Chrome/83.0.4103.97 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,'
                      'application/xml;q=0.9,image/webp,'
                      'image/apng,*/*;q=0.8,application/signed-exchange;'
                      'v=b3;q=0.9',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        }
    )
    # pattern = re.compile(r'\<span class="title"\>(?P<title>[\u4e00-\u9fa50-9：]*?)\<\/span\>')
    # items = pattern.findall(resp.text)
    # for item in items:
    #     print(item)
    # 创建BeautifulSoup对象来进行页面解析
    soup = bs4.BeautifulSoup(resp.text, features='lxml')
    # 获取包含电影信息的a标签
    elements = soup.select('.info>div>a')
    for element in elements:
        # 获取a标签下class属性为title的span标签`
        span = element.select('.title')[0]
        # 获取span标签的内容
        print(span.text)
    # 随机休眠一段时间避免爬取过于频繁
    time.sleep(random.random() * 5)
