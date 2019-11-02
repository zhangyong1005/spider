# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
from selenium import webdriver
import time
import scrapy
# from retrying import retry

class TqMiddleware(object):
    # @retry(max_fixed=200,stop_max_attempt_number=4)
    # def retry_load_data(self,request,spider):
    #     self.driver.find_element_by_xpath('//tr/td/a/@href')


    def process_request(self, request, spider):
        self.driver = webdriver.Chrome()
        # 判断动态页面采用 selenium+Chrome抓取
        if request.url != "https://www.aqistudy.cn/historydata/":
            self.driver.get(request.url)
            # self.retry_load_data()
            time.sleep(3)

            html = self.driver.page_source
            self.driver.quit()
            # 构造返回response响应体
            return scrapy.http.HtmlResponse(url=request.url, body=html,
                                        encoding="utf-8",request=request)