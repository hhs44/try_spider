from collections import deque
from concurrent.futures.thread import ThreadPoolExecutor
from threading import RLock
from urllib.parse import urljoin

import bs4
import requests

import MySQLdb
from MySQLdb.cursors import DictCursor
import datetime

MAX_DEPTH = 3
visited_urls = set()
new_urls = deque()
lock = RLock()

def fix_url(curr_url, href):
    if href.startswith('//'):
        href = f'http:{href}'
    elif href.startswith('/'):
        href = urljoin(curr_url, href)
    href = href.replace('!\'\'}', '')
    return href if href.startswith('http') or href.startswith('https') else ''


def fetch_page(curr_url, depth):
    try:
        resp = requests.get(curr_url, timeout=1)
    except Exception as ex:
        print(ex)
    else:
        soup = bs4.BeautifulSoup(resp.text, 'lxml')
        if depth < MAX_DEPTH:
            all_anchors = soup.find_all('a')
            with lock:
                for anchor in all_anchors:
                    href = anchor.attrs.get('href', '')
                    href = fix_url(curr_url, href)
                    if href:
                        print(href)
                        new_urls.append((href, depth + 1))
            visited_urls.add(curr_url)
            
def main():
    seed_url = 'https://sports.sohu.com/'
    new_urls.append((seed_url, 0))
    with ThreadPoolExecutor(max_workers=32) as pool:
        while len(new_urls) > 0 or len(visited_urls) == 0:
            print(len(new_urls))
            if len(new_urls) > 0:
                with lock:
                    curr_url, depth = new_urls.popleft()
                if curr_url not in visited_urls:
                    pool.submit(fetch_page, curr_url, depth)
                    
                    

conn = MySQLdb.connect(host='123.56.80.63',
                      port=3306,
                      user='root',
                      passwd='mysql',
                      db='crawel',
                      charset='utf8')
t = datetime.datetime.now()
