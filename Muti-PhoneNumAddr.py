# 2018年9月21日21点20分, @HDU Dorm 602
# 尝试爬取手机号码归属地
# 为了10月份中旬找杭州的人一起去北京RTT发布会
# 大概有40万条数据
# 尝试多进程爬取
# ToDoList：
# 1. 保存操作在程序结尾，中途中断就前功尽弃

import re
import time
import xlwt
import requests
from multiprocessing import Pool

# 手机号码归属地由前七位决定
HeadList = ['139', '138', '137', '136', '135', '134', '159', '158', '157', '150',
            '151', '152', '188', '187', '182', '183', '184', '178', '147', '170',
            '130', '131', '132', '156', '155', '186', '185', '176', '175', '145',
            '171', '133', '134', '153', '189', '180', '181', '177', '173', '149',
            ]


headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}

book = xlwt.Workbook(encoding='utf-8')
sheet = book.add_sheet('Sheet1')
# sheet.write(#行，#列，#内容)
sheet.write(0, 0, '号段')
sheet.write(0, 1, '归属地')
count = 0


def get_data(PhoneNum):
    global count
    count += 1
    # time.sleep(1)
    # 经观察，直接构造手机号的URL, 返回的就是手机号归属地
    url = "http://www.ip138.com:8080/search.asp?mobile={}&action=mobile".format(PhoneNum)
    # print(url)
    res = requests.get(url=url, headers=headers)
    # print(res.encoding)
    # print(res.apparent_encoding)
    # print(requests.utils.get_encodings_from_content(res.text)[0])
    text = res.text.encode('ISO-8859-1').decode(requests.utils.get_encodings_from_content(res.text)[0])
    # print(text)
    # 清洗源码，提取地址
    Addr = re.findall('卡号归属地</TD>(.*?)</TD>', text, re.S)
    # print(Addr)
    if Addr != []:
        Addr = re.sub("[A-Za-z0-9\"=<>!\-*&;/]", '', Addr[0])
        Addr = Addr.strip()
        print(PhoneNum, Addr)
        sheet.write(count, 0, PhoneNum)
        sheet.write(count, 1, Addr)

    else:
        print(PhoneNum, '非法号段')
        sheet.write(count, 0, PhoneNum)
        sheet.write(count, 1, '非法号段')


def generate_num(Head):
    for i in range(0, 10000):
        PhoneNum = Head + str(i).zfill(4)
        get_data(PhoneNum)


def main():
    pool = Pool(processes=4)
    pool.map(func=generate_num, iterable=HeadList)

    book.save('Muti-手机号归属地.xls')


if __name__ == "__main__":
    main()

