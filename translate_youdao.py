import urllib.request
import urllib.parse
import json
import time
import random
import hashlib


# headers = {
# "Cookie":" OUTFOX_SEARCH_USER_ID=1449344671@10.108.160.14",
# "Referer": "http://fanyi.youdao.com/",
# "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3730.400 QQBrowser/10.5.3805.400",
# }
# url = 'http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'
# u = 'fanyideskweb'
# d = content
# f = str(int(time.time()*1000)*10 + random.randint(1,9))
# c = 'n%A-rKaT5fb[Gy?;N5@Tj'
# sign = hashlib.md5((u + d + f + c).encode('utf-8')).hexdigest()
# data = {
#     "i": d,
#     "client": "fanyideskweb",
#     "doctype": "json",
#     "salt": f,
#     "sign": sign,
#     "version": "2.1",
#     "keyfrom": "fanyi.web",
# }
# data = urllib.parse.urlencode(data).encode('utf-8')
# request1 = urllib.request.Request(url=url,data=data,headers=headers)
# response = urllib.request.urlopen(request1)
# html=response.read().decode('utf-8')
# json_data=json.loads(html)
# print(json_data.get("translateResult")[0][0].get("tgt"))

class YoudaoSpider(object):

    def __init__(self):
        self.url = 'http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'
        self.headers = {
            "Cookie": " OUTFOX_SEARCH_USER_ID=1449344671@10.108.160.14",
            "Referer": "http://fanyi.youdao.com/",
            "User-Agent": self.getheaders(),
        }
        self.content = input('请输入需要翻译的句子：')
        u = 'fanyideskweb'
        d = self.content
        f = str(int(time.time() * 1000) * 10 + random.randint(1, 9))
        c = 'n%A-rKaT5fb[Gy?;N5@Tj'
        sign = hashlib.md5((u + d + f + c).encode('utf-8')).hexdigest()
        data = {
            "i": d,
            "client": "fanyideskweb",
            "doctype": "json",
            "salt": f,
            "sign": sign,
            "version": "2.1",
            "keyfrom": "fanyi.web",
        }
        self.data = urllib.parse.urlencode(data).encode('utf-8')

    def getheaders(self):
        user_agent_list = [
            'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1464.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.16 Safari/537.36',
            'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.3319.102 Safari/537.36',
            'Mozilla/5.0 (X11; CrOS i686 3912.101.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36',
            'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:17.0) Gecko/20100101 Firefox/17.0.6',
            'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1468.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2224.3 Safari/537.36',
            'Mozilla/5.0 (X11; CrOS i686 3912.101.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36']
        UserAgent = random.choice(user_agent_list)
        return UserAgent

    def main(self):
        request1 = urllib.request.Request(url=self.url, data=self.data, headers=self.headers)
        response = urllib.request.urlopen(request1)
        html = response.read().decode('utf-8')
        json_data = json.loads(html)
        print(json_data.get("translateResult")[0][0].get("tgt"))

if __name__ == '__main__':
    a=YoudaoSpider()
    a.main()
