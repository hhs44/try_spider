import requests
# from pyvirtualdisplay import Display
from bs4 import BeautifulSoup
from pandas import DataFrame
import re
import time
import csv
from selenium import webdriver
# import matplotlib.pyplot as plt

# display = Display(visible=0, size=(800, 600))
# display.start()
driver = webdriver.Chrome('chromedriver.exe')
driver.get("https://yz.chsi.com.cn/zsml/queryAction.do")


# #获取省份，专业，信息
# province = driver.find_element_by_id("ssdm")
# options_list = province.find_elements_by_tag_name("option")
# options = []
# for option in options_list:
#     options.append(option.text)
# with open("province_list.txt","w+",encoding="utf-8") as f:
#     for i in options:
#         if i !="选择省市":
#             f.write(i+"\n")
#
# subject = driver.find_element_by_id("yjxkdm")
# options_list1 = subject.find_elements_by_tag_name("option")
# option1 = []
# for option in options_list1:
#     option1.append(option.text)
# with open("subject_list.txt","w+",encoding="utf-8") as f:
#     for i in option1:
#         if i != "选择学科类别":
#             f.write(i+"\n")
# driver.quit()
# #输入查询信息
# with open("province_list.txt","r",encoding="utf-8") as f:
#     str = f.readlines()
#     linesnew = []
#     for line in str:
#         line1 = line.split('\n')
#         linesnew.append(line1[0])
#     p1 = input("是否查看所有省市（是/否）：")
#     if p1 == "是":
#         print(linesnew)
# with open('subject_list.txt',"r",encoding="utf-8")as f:
#     str1 = f.readlines()
#     linesnew1 = []
#     for line2 in str1:
#         line3 = line2.split('\n')
#         linesnew1.append(line3[0])
#     p2 = input("是否查看所有招收专业（是/否）：")
#     if p2 == "是":
#         print(str1)

class Graduate:
    # 发送请求获取数据
    def __init__(self, province, subject):
        self.head = {
            "User_Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36"}
        self.data = []
        self.privence = province
        self.subject = subject

    def get_school_url(self):
        # POST请求
        # 返回学校网址
        url = "https://yz.chsi.com.cn/zsml/queryAction.do"
        datas = {'ssdm': self.privence, 'yjxkdm': self.subject}

        response = requests.post(url, data=datas, headers=self.head)
        html = response.text
        reg = re.compile(r'(<tr>.*? </tr>)', re.S)
        content = re.findall(reg, html)
        # 正则表达式提取学校网址
        schools_url = re.findall('<a href="(.*?)" target="_blank">.*?</a>', str(content))

        return schools_url

    # 返回一个学校所有学院的数据，正则表达式提取
    def get_college_data(self, url):
        response = requests.get(url, headers=self.head)
        html = response.text
        colleges_url = re.findall('<td class="ch-table-center"><a href="(.*?)" target="_blank">查看</a>', html)
        return colleges_url

    def get_final_data(self, url):
        temp = []
        response = requests.get(url, headers=self.head)
        html = response.text
        soup = BeautifulSoup(html, features='html')

        summary1 = soup.find_all('td', {"class": "zsml-summary"})
        summary2 = soup.find_all('span', {"class": "zsml-bz"})
        summary = summary1 + summary2
        for x in summary:
            temp.append(x.get_text())
        self.data.append(temp)

    # 获取所有学校的数据
    def get_schools_data(self):
        url = "https://yz.chsi.com.cn"
        schools_urls = self.get_school_url()
        amount = len(schools_urls)
        i = 0
        for schools_url in schools_urls:
            i += 1
            url2 = url + schools_url
            colleges_url = self.get_college_data(url2)
            print("已完成第" + str(i) + "/" + str(amount) + "学院爬取")
            time.sleep(2)
            for college_url in colleges_url:
                url3 = url + college_url
                self.get_final_data(url3)

        # 保存数据

    def get_data_frame(self):
        data1 = []
        headers = ['学校', '考试方向', '院系', '其他', '专业代码', '学习方式', '研究方向', '指导老师', '拟招人数']
        with open("招生信息查询.csv", 'w', newline='') as f:
            writer = csv.DictWriter(f, headers)
            writer.writeheader()
            for row in data1:
                writer.writerow(row)
        data = DataFrame(self.data)
        data.to_csv("招生信息查询.csv", header=None, index=None, mode='a', encoding='gbk')


if __name__ == '__main__':
    province = input("请输入查询学校省份编号：")
    subject = input("请输入查询专业编号：")
    demo = Graduate(province, subject)
    demo.get_schools_data()
    demo.get_data_frame()
