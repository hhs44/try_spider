from bs4 import BeautifulSoup
import requests
import re
import time
from selenium import webdriver


driver = webdriver.Chrome('chromedriver.exe')
driver.get("https://www.zhipin.com/job_detail/?query=")

# 获取所有的工作类型
job = driver.find_element_by_xpath('//*[@id="filter-box"]/div/div[1]/div/form/div[5]/div/div/ul[1]')
job_tree1 = job.find_elements_by_tag_name("li")
for x in job_tree1:
    print(x.text)
