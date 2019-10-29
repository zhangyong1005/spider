import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from lxml import etree

url = 'https://www.xinpianchang.com/channel/index/sort-like?from=tabArticle'
html = requests.get(url)
soup = BeautifulSoup(html.text, 'lxml')
titles = soup.select('div.video-con-top>a>p')
types = soup.select('div.video-con-top>div.new-cate')
watchs = soup.select('.video-view>span')[::2]
likes = soup.select('.video-view>span')[1::2]
people = soup.select('.user-info')
imgs = soup.select('a.video-cover>img')
url2 = soup.select('li.enter-filmplay')
sum = 1
for title, type, watch, like, person, img, li in zip(titles, types, watchs, likes, people, imgs, url2):
    print(sum)
    print('标题：' + title.text)
    print('视频来源：' + type.text.strip().replace('\n', '').replace('\t' * 4, '').replace('\t' * 2, '|'))
    print('观看数：' + watch.text.strip())
    print('点赞数：' + like.text.strip())
    print('图片：' + img.get('_src'))
    print(person.text.strip().replace('\n' * 11, '\n').replace('\t' * 4, '').replace('\t' * 2, '\t').replace('\n' * 2,
                                                                                                             '\n'))
    two_url = 'https://www.xinpianchang.com/a' + li.get('data-articleid')
    driver = webdriver.Chrome()
    driver.get(two_url)
    new_html = driver.page_source
    html_obj = etree.HTML(new_html)
    video = html_obj.xpath("//video/@src")[0]
    print('视频地址:' + video)
    mp4 = requests.get(video)
    with open('%s.mp4' % li.get('data-articleid'), 'wb+')as w:
        w.write(mp4.content)
    driver.quit()
    print('-----------------分割----------------------')
    sum += 1


