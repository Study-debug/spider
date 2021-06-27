# encoding=utf-8
"""
作者：MR.king
日期：2021年06月27日
"""

'''
    需求: 爬取梨视频
    原则: 只用来处理处理阻塞且耗时的操作
    https://video.pearvideo.com/mp4/third/20210624/cont-1733207-12719568-220616-hd.mp4
    https://video.pearvideo.com/mp4/third/20210624/1624796573950-12719568-220616-hd.mp4
'''
from lxml import etree
import re
import requests
import random
import json
from multiprocessing import Pool

def get_data(dic):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0',
    }
    url = dic["url"]
    print(dic['name'], "正在下载...")
    data = requests.get(url=url, headers=headers).content
    with open("./resources/梨视频/" + dic["name"], "wb") as fp:
        fp.write(data)
        print(dic['name'], "下载成功！")


if __name__ == '__main__':
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0'}
    # 对此页面发请求获取视频url 以及名字
    url = 'https://www.pearvideo.com/category_59'
    page_text = requests.get(url=url, headers=headers).text
    tree = etree.HTML(page_text)
    li_list = li_list = tree.xpath('//ul[@id="listvideoListUl"]/li[@class="categoryem "]')
    urls = []
    for li in li_list:
        page_url = 'https://www.pearvideo.com/' + li.xpath('./div/a/@href')[0]
        # print(page_url)
        name = li.xpath('./div/a/div[2]/text()')[0] + '.mp4'
        # print(name)
        cotent = requests.get(url=page_url, headers=headers).text
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0',
            "Referer": page_url
        }
        cont_id = re.findall(r"_(.+)", page_url)[0]  # 在page_url中拿到id
        # 该请求需要生成随机数
        params = {
            "contId": cont_id,
            "mrd": str(random.random())
        }
        # 基础网址 https://www.pearvideo.com/videoStatus.jsp?contId=1733335&mrd=0.773280683409967
        url = "https://www.pearvideo.com/videoStatus.jsp"
        response = requests.get(url=url, headers=headers, params=params).json()
        src_url = response["videoInfo"]["videos"]["srcUrl"]  # 获取json中的srcurl
        # 处理拿到的url
        src_url_list = src_url.split("/")
        src_url_list_last = src_url_list[-1]
        last_list = src_url_list_last.split("-")
        last_list[0] = "cont-" + cont_id
        last = "-".join(last_list)
        src_url_list[-1] = last
        new_src_url = "/".join(src_url_list)
        dic = {
            "name": name,
            "url": new_src_url
        }
        urls.append(dic)
        # 多线程下载
        pool = Pool(4)
        pool.map(get_data, urls)
        pool.close()
        pool.join()


