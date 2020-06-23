import aiohttp
import asyncio
import re

pattern = re.compile('<title>(?P<foo>.*?)</title>')
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/83.0.4103.97 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;'
              'q=0.9,image/webp,image/apng,*/*;'
              'q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
}


async def fetch_page(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers, ssl=False) as resp:
            page_html = await resp.text()
            match = pattern.search(page_html)
            print(match.group('foo'))


def main():
    loop = asyncio.get_event_loop()
    urls = [
        'https://www.douban.com/',
        'http://www.sohu.com/',
        'http://www.sina.com.cn/',
        'https://www.taobao.com/',
        'http://jd.com/',
        'https://www.python.org/',
        'https://github.com/',
        'https://www.linkedin.com/',
        'https://leetcode.com/',
        'https://pypi.org/',
    ]
    tasks = [fetch_page(url) for url in urls]
    # print(tasks)
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()


if __name__ == "__main__":
    main()
