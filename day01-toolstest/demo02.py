import random
import time

import bs4
import requests
from lxml import etree

headers ={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                  ' AppleWebKit/537.36 (KHTML, like Gecko)'
                  ' Chrome/83.0.4103.97 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,'
              'application/xml;q=0.9,image/webp,'
              'image/apng,*/*;q=0.8,application/signed-exchange;'
              'v=b3;q=0.9',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
}

# url = 'https://mil.news.sina.com.cn/'
#
#
# resp = requests.get(url=url, headers=headers)
# soup = bs4.BeautifulSoup(resp.text, features='lxml')
# elements = soup.select('a')
# for x, element in enumerate(elements):
#     # print(type(element.text))
#     print(element.text)

resp = requests.get(
    url='https://mil.news.sina.com.cn/',
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
    }
)
tree = etree.HTML(resp.content.decode('utf-8'))
href_list = tree.xpath('//div[@class="zgjq"]/div[@class="left"]/ul/li/a/@href')
content_list = tree.xpath('//div[@class="zgjq"]/div[@class="left"]/ul/li/a/text()')

image_list = tree.xpath('//div[@class="photo-content"]//li/a/img/@src')
images = []
for image in image_list:
    image = 'https:' + image
    images.append(image)


print(href_list)
print(content_list)
print(images)