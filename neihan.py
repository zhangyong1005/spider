import re
import requests
headers={
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3730.400 QQBrowser/10.5.3805.400'
}
for i in range(1,507):
    url='https://www.neihan-8.com/article/list_5_%d.html'%i
    response=requests.get(url,headers=headers)
    html=response.content.decode('gbk')
    r0=r'<a href="/article/\d+.html">(.*?)</a>'
    titles0=re.findall(r0,html)
    for index,k in enumerate(titles0):
        titles0[index]=re.compile(r'[(</*b>)+]').sub('',k)
    r2=r'<div class="f18 mb20">(.*?)</div>'
    tz=re.findall(r2,html,re.S)
    for index,j in enumerate(tz):
        tz[index]=re.compile(r'\s').sub('',j)
        tz[index] = re.compile(r'<br/>').sub('\n', tz[index])
        tz[index] = re.compile(r'[(</*p>)+]|&\w+;').sub('', tz[index])
    for title,text1 in zip(titles0,tz):
        num=titles0.index(title)+1
        with open('neihan.txt','a',encoding='utf-8')as f:
            f.write('第%s页第%s篇'%(i,num)+'\n标题：'+title+'\n'+text1+'\n'+'----------分割----------\n')
    print('第%s页'%i+'完成')
    input('请输入回车爬取下一页')