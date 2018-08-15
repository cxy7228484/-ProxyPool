#!/usr/bin/python3
# -*- coding: utf-8 -*-

import requests
from lxml import etree

class Daili66ProxySpider(object):

    def get_url_list(self):
        return ["http://www.66ip.cn/{}.html".format(i) for i in range(1,10)]


    def get_proxies(self):
        headers = {
            "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
        }
        for url in self.get_url_list():
            response = requests.get(url,headers=headers)
            edata = etree.HTML(response.text)
            rows = edata.xpath('//table//tr')
            for idx in range(2,len(rows)):
                row = rows[idx]
                ip = row.xpath('./td[1]/text()')[0]
                port = row.xpath('./td[2]/text()')[0]
                yield "http://{}:{}".format(ip,port)
                yield "https://{}:{}".format(ip,port)