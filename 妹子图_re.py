"""
作者：MR.king
日期：2021年06月05日
"""
'''
    <h2>
    <a target="_blank" href="https://www.mm618.com/albums/12774">超紧致美臀致命诱惑！极品水嫩美女芝芝Booty香艳私拍</a>
    </h2>
    https://img.mm618.com/photos/238680/27c01.jpg
    https://img.mm618.com/photos/238680/27c02.jpg
    https://img.mm618.com/photos/241017/11b01.jpg
'''
import requests
import re

if __name__ == '__main__':
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0'}
    all_page = input('please input  all_img  page:  ')
    url = 'https://www.mm618.com/page/' + all_page
    response = requests.get(url=url, headers=headers).text
    # print(response)
    # xe = '<h2>.*?(https://www.mm618.com/albums/\d{5}).*?</h2>'
    xe = '<h2>.*?href="(.*?)">.*?</h2>'
    href_url_list = re.findall(xe, response, re.S)
    print(href_url_list)
    img_data = []
    img_name = []
    start = int(input('please input the start img_page:  '))
    end = int(input('please input the end  img_page:  '))
    print('数据解析中,请稍等...')
    for page in href_url_list:
        # print(page)
        for index in range(start, end):
            index = page + '/' + str(index)
            # print(index)
            img_response = requests.get(url=index, headers=headers).text
            img_xe = '<p>.*?src="(.*?)" alt.*</p>'
            img_url = re.findall(img_xe, img_response, re.S)
            img_data.append(img_url)
    for data in img_data:
        # print(data[0])
        url = data[0]
        data_response = requests.get(url=url, headers=headers).content
        img_name = str(data[0]).split('/')[-1]
        with open('./resources/妹子图/' + img_name, 'wb+') as fp:
            fp.write(data_response)
            print(img_name, '下载完成！')
print('抓取结束')
