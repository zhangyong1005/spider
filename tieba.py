import random
import re
import os
import time
import requests
from bs4 import BeautifulSoup
import urllib.request
def getheaders():
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
start_page=(int(input('请输入起始页：'))-1)*50
end_page=(int(input('请输入结束页：')))*50
name=input('请输入要爬取的贴吧名：')
name_url = urllib.request.quote(name)
for k in range(start_page, end_page, 50):
    t=int(k//50+1)
    u_name = 'https://tieba.baidu.com/f?ie=utf-8&kw=' + name_url + '&ie=utf-8&pn=' + str(k)
    root = "D://tieba//%s%s//" %(name,str(k // 50 + 1))
    if not os.path.exists(root):
        os.mkdir(root)
    request=urllib.request.Request(u_name)
    request.add_header("User-agent", getheaders())
    url = urllib.request.urlopen(request)
    html = url.read().decode().replace('<!--','').replace('-->','')
    soup = BeautifulSoup(html, 'lxml')
    list1 = soup.find_all('li')
    for i in list1:
        try:
            l1 = i.div.find_all('div')[1].div.div.a.get('href')
            title = i.div.find_all('div')[1].div.div.a.get_text()
            l3 = i.div.find_all('div')[1].div.find_all('div')[1].span.get('title')
            with open(root + 'tieba.txt', 'a+', encoding='utf-8')as f:
                f.write('主题内容' + title + '\n')
                f.write(l3 + '\n')
            two_url = 'https://tieba.baidu.com' + l1
            html2 = requests.get(two_url)
            soup2 = BeautifulSoup(html2.text, 'lxml')
            list3 = soup2.select('li >span.red')[1]
            page=int(list3.get_text())+1
            for p in range(1,page):
                three_url=two_url+'?pn=%s'%str(p)
                list2 = soup2.select('.d_post_content_main')
                for k in list2:
                    img = k.find_all('img')
                    if img:
                        for j in img:
                            url_img = re.compile(r'^//.*').sub('', j.get('src'))
                            if url_img:
                                with open(root + 'tieba.txt', 'a+', encoding='utf-8')as f:
                                    f.write(url_img + '\n')
                                path = root + url_img.split('/')[-1]
                                try:
                                    if not os.path.exists(path):
                                        r = requests.get(url_img)
                                        with open(path, 'wb')as f:
                                            f.write(r.content)
                                            print("文件保存成功")
                                    else:
                                        print("文件已存在")
                                except:
                                    print("爬取失败")
        except AttributeError:
            pass
        except IndexError:
            pass
    print('第%d页爬完' %t)
    print('-------------')
    time.sleep(1)
