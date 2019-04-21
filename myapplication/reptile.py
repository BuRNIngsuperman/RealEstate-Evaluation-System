from  bs4 import BeautifulSoup
import requests
import re
import time


def Reptile(num):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}

    # 设置列表页URL的固定部分
    url = 'http://sh.lianjia.com/ershoufang/'
    # 设置页面页的可变部分
    page = ('pg')
    # 循环抓取列表页信息
    for i in range(1, num):
        if i == 1:
            i = str(i)
            a = (url + page + i + '/')
            r = requests.get(url=a, headers=headers)
            html = r.content
        else:
            i = str(i)
            a = (url + page + i + '/')
            r = requests.get(url=a, headers=headers)
            html2 = r.content
            html = html + html2
        # 每次间隔0.5秒
        time.sleep(0.5)
    # 解析抓取的页面内容
    lj = BeautifulSoup(html, 'html.parser')
    price = lj.find_all('div', attrs={'class': 'totalPrice'})
    tp = []
    for a in price:
        totalPrice = a.span.string
        tp.append(totalPrice)
    unit_price = lj.find_all('div', attrs={'class': 'unitPrice'})
    up = []
    for b in unit_price:
        unitprice = b.span.string
        up.append(unitprice)
    position = lj.find_all('div', attrs={'class': 'positionInfo'})
    ps = []
    for d in position:
        positioninfo = d.get_text()
        ps.append(positioninfo)
    # 提取房源信息
    houseInfo = lj.find_all('div', attrs={'class': 'houseInfo'})

    hi = []
    for c in houseInfo:
        house = c.get_text()
        hi.append(house)
    # 导入pandas库
    import pandas as pd
    # 创建数据表
    house = pd.DataFrame({'price': tp, 'unit_price': up, 'houseinfo': hi, 'position': ps})
    # 对房源信息进行分列
    houseinfo_split = pd.DataFrame((x.split('|') for x in house.houseinfo), index=house.index,
                                   columns=['xiaoqu', 'huxing', 'mianji', 'chaoxiang', 'zhuangxiu', 'dianti', 'error'])
    houseinfo_split.drop(['error'], axis=1, inplace=True)
    # 将分列结果拼接回原数据表
    house = pd.merge(house, houseinfo_split, right_index=True, left_index=True)
    house.drop(['houseinfo'], axis=1, inplace=True)
    position_split = pd.DataFrame((x.split('-') for x in house.position), index=house.index,
                                  columns=['house_type', 'area', ])
    # 将分列结果拼接回原数据表
    house = pd.merge(house, position_split, right_index=True, left_index=True)
    house.drop(['position'], axis=1, inplace=True)
    return house

if __name__=="__main__":
    input_page=input("输入爬取页数：")
    num=int(input_page)
    re_data=Reptile(num)
    re_data.to_csv("D:\\djangotest\\挂牌.csv",encoding="utf-8")
    data=re_data.values.tolist()
    print(data)

