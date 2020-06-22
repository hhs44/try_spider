import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

options = webdriver.ChromeOptions()
# 添加参数启动无头浏览器（没有浏览器界面）
options.add_argument('headless')
chrome = webdriver.Chrome(options=options)
chrome.get('https://image.so.com/')
search_input = chrome.find_element_by_css_selector('#search_kw')
search_input.send_keys('美女')
search_input.send_keys(Keys.RETURN)
for pos in range(1, 20):
    chrome.execute_script(f'window.scrollTo(0, {pos * 3000})')
    time.sleep(2)
    # wait = WebDriverWait(chrome, 10)
    # wait.until(expected_conditions.presence_of_all_elements_located((By.TAG_NAME, 'img')))
images = chrome.find_elements_by_css_selector('span.img>img')
for image in images:
    print(image.get_attribute('src'))
chrome.quit()


