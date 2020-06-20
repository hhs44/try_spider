import hashlib
import io
from collections import deque
from concurrent.futures.thread import ThreadPoolExecutor
from threading import local
from urllib.parse import urljoin, urlparse

import MySQLdb
import bs4
import requests

MAX_DEPTH = 2

visited_urls = set()
new_urls = deque()
seed_url = 'https://sports.sohu.com/'
netloc = urlparse(seed_url).netloc


def _force_bytes(data):
    if type(data) != bytes:
        if type(data) == str:
            data = data.encode()
        elif type(data) == io.BytesIO:
            data = data.getvalue()
        else:
            data = bytes(data)
    return data


def make_md5_digest(data):
    """生成MD5摘要"""
    data = _force_bytes(data)
    return hashlib.md5(data).hexdigest()


def get_db_connection():
    thread_local = local()
    if not hasattr(thread_local, 'conn'):
        conn = MySQLdb.connect(host='123.56.80.63', port=3306,
                               user='root', password='mysql',
                               database='crawel', charset='utf8',
                               autocommit=True)
        setattr(thread_local, 'conn', conn)
    return getattr(thread_local, 'conn')


def write_to_db(url, content, digest):
    with get_db_connection().cursor() as cursor:
        cursor.execute(
            'insert into news (url, content, digest) values (%s, %s, %s)',
            (url, content, digest)
        )


def fix_url(curr_url, href):
    if href.startswith('//'):
        href = f'http:{href}'
    elif href.startswith('/'):
        href = urljoin(curr_url, href)
    elif href.startswith('mailto') or href.startswith('javascript')\
            or href.startswith('#') or href.startswith('?'):
        href = ''
    href = href.replace('!\'\'}', '')
    return urljoin('http://', href) if href else href


def fetch_page(curr_url, depth):
    try:
        resp = requests.get(curr_url, timeout=1)
    except Exception as ex:
        print(ex)
    else:
        write_to_db(curr_url, resp.text, make_md5_digest(resp.text))
        soup = bs4.BeautifulSoup(resp.text, 'lxml')
        if depth < MAX_DEPTH:
            all_anchors = soup.find_all('a')
            for anchor in all_anchors:
                href = anchor.attrs.get('href', '')
                href = fix_url(curr_url, href)
                
                if urlparse(href).netloc == netloc:
                    print(href)
                    new_urls.append((href, depth + 1))
                    


def main():
    new_urls.append((seed_url, 0))
    with ThreadPoolExecutor(max_workers=32) as pool:
        future = None
        while len(new_urls) > 0 or (future and not future.done()):
            # print(new_urls)
            if len(new_urls) > 0:
                curr_url, depth = new_urls.popleft()
                if curr_url not in visited_urls:
                    visited_urls.add(curr_url)
                    future = pool.submit(fetch_page, curr_url, depth)


if __name__ == '__main__':
    main()