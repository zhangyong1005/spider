import time

import requests
import execjs
from fake_useragent import UserAgent
import pymysql

conn = pymysql.connect(host='127.0.0.1', port=3306,
                       user='root', passwd='root',
                       db='jijin', charset='utf8')
cursor = conn.cursor()
headers = {"user-agent": UserAgent().random}
for page in range(0,116):
    url = 'http://fund.eastmoney.com/data/rankhandler.aspx?op=ph&dt=kf&ft=all&rs=&gs=0&sc=zzf&st=desc&sd=2019-02-05&ed=2020-02-05&qdii=&tabSubtype=,,,,,&pi='+str(page)+'&pn=50&dx=1'
    html = requests.get(url, headers=headers)
    data_json = execjs.compile(html.text)
    datas = data_json.eval('rankData')
    for data in datas['datas']:
        list1 = data.split(',')
        # 基金代码
        number = list1[0]
        # 名字
        name = list1[1]
        # 日期
        now_date = list1[3][:5]
        # 单位净值
        one_value = list1[4][:5]
        # 累计净值
        all_value = list1[5][:5]
        # 日增长
        day_up = list1[6][:5]
        # 近一周
        one_week = list1[7][:5]
        # 近一月
        one_mouth = list1[8][:5]
        # 近三月
        three_mouth = list1[9][:5]
        # 近六月
        six_mouth = list1[10][:5]
        # 近一年
        one_year = list1[11][:5]
        # 近两年
        two_year = list1[12][:5]
        # 近三年
        three_year = list1[13][:5]
        # 今年来
        this_year = list1[14][:5]
        # 成立来
        set_up = list1[15][:5]
        # 自定义
        custom = list1[18][:5]
        # 手续费
        fee = list1[20][:5]
        cursor.execute(
            "insert into fund_list(number,name,now_date,one_value,all_value,day_up,one_week,one_mouth,three_mouth,six_mouth,one_year,two_year,three_year,this_year,set_up,custom,fee)values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s') " % (
            number, name, now_date, one_value, all_value, day_up, one_week, one_mouth, three_mouth, six_mouth, one_year,
            two_year, three_year, this_year, set_up, custom, fee)
        )
    print('第%s页完成'%(page+1))
    time.sleep(2)
conn.commit()
cursor.close()
conn.close()
print('全部完成')
