# !/user/bin/python
# coding:utf-8

# 做网页分析的 bs4
# pip install bs4

# 解析网页
# pip install lxml

# 用来做网络请求的
# pip install requests

# 用来做网络图表的库
# pip install echarts-python

# 1.第一步：把网页数据全部抓取下来（requests）
# 2.第二步：把抓下来的数据进行过滤，把需要的数据提取出来，把不需要的给过滤掉（bs4）

from bs4 import BeautifulSoup
import requests
import time
from echarts import Echart,Bar,Axis
import json

# 定义全局变量保存数据
TEMPERATURE_LIST = []
CITY_LIST = []
MIN_LIST = []

# get/post
# request header

def get_temperature(url):
    header = {
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) \
        Chrome/60.0.3112.113 Safari/537.36',
        'Upgrade-Insecure-Requests':'1',
        # 'Referer':'http://www.weather.com.cn/textFC/hb.shtml',
        'Host':'www.weather.com.cn'
    }

    # html = "http://www.weather.com.cn/textFC/hb.shtml"
    req = requests.get(url,headers=header)
    # req = req.encode('gbk','ignore')
    # print (req.content)

    """
    所有的城市都是放在所属省份或直辖市的表格中
    真正有用的数据是从第2个tr开始的（下标从0开始）
    真正有用的第0个tr中的第0个td, 表示的是当前这个表格的省份或直辖市的名字
    其余有用的tr是第0个td, 实际上就是表示了当前这个城市的名字
    """
    # 获取页面
    content = req.content
    soup = BeautifulSoup(content,'lxml')

    # 获取省份
    conMid_tab = soup.find('div',class_='conMidtab')
    conMid_list = conMid_tab.find_all('div',class_='conMidtab2')
    for x in conMid_list:
        tr_list = x.find_all('tr')[2:]
        # print(tr_list)
        # 获取城市
        for index,tr in enumerate(tr_list):
        # 如果是第0个tr标签，那么城市和省份名是放在一起的
            if index == 0:
                td_list = tr.find_all('td')
                province = td_list[0].text.replace('\n',' ')  # 省份
                city = td_list[1].text.replace('\n',' ')    # 城市
                minW = td_list[7].text.replace('\n',' ')     # 最低气温
        # 如果不是第0个tr标签，那么在这个tr标签中只存放城市名
            else:
                td_list = tr.find_all('td')
                city = td_list[0].text.replace('\n',' ')    # replace('\n',' ')删除换行
                minW = td_list[6].text.replace('\n',' ')     # 最低气温

            # print('%s|%s' % (province+city, minW))
            TEMPERATURE_LIST.append({
                'city':province+city,
                'minW':minW
            })
            CITY_LIST.append(province+city)
            MIN_LIST.append(minW)

def main():
    # 华北、东北、华东，华中、华南、西南地区的 url
    urls = ['http://www.weather.com.cn/textFC/hb.shtml',
            'http://www.weather.com.cn/textFC/db.shtml',
            'http://www.weather.com.cn/textFC/hd.shtml',
            'http://www.weather.com.cn/textFC/hz.shtml',
            'http://www.weather.com.cn/textFC/hn.shtml',
            'http://www.weather.com.cn/textFC/xn.shtml']

    for url in urls:
        get_temperature(url)
        time.sleep(2)

    # 存储成json文件
    # line = json.dumps(TEMPERATURE_LIST,ensure_ascii=False)
    # with open('temperature.json','w') as fp:
    #     fp.write(line.encode('utf-8'))

    TOP20_CITY_LIST = CITY_LIST[0:10]
    TOP20_MIN_LIST = MIN_LIST[0:10]

    # 图表显示
    echart = Echart(u'全国最低温度排名',u'中国天气网提供')
    bar = Bar(u'最低温度', TOP20_MIN_LIST)
    axis = Axis('category','bottom', data=TOP20_CITY_LIST)
    echart.use(bar)
    echart.use(axis)
    echart.plot()

if __name__ == '__main__':
    main()