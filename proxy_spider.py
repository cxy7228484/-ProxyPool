#!/usr/bin/python3
# -*- coding: utf-8 -*-



import importlib

import settings

import redis_proxy_pool

class ProxySpider(object):
    def __init__(self):
        self.pool = redis_proxy_pool.RedisProxyPool()
        pass

    def _auto_import_instances(self, paths=[]):
        instances = []
        for path in paths:
            module_name = path.rsplit('.', 1)[0]
            cls_name = path.rsplit('.', 1)[1]
            module = importlib.import_module(module_name)
            cls = getattr(module, cls_name)
            instances.append(cls())
        return instances

    # 处理代理
    def process_proxy_spiders(self):
        # 获取代理爬虫
        spiders = self._auto_import_instances(settings.PROXIES_SPIDERS)

        # 执行爬虫获取代理
        for spider in spiders:
            try:
                proxies = spider.get_proxies()
                if proxies is not None:
                    for proxy in proxies:
                        print("爬取代理",proxy,"添加到代理池中")
                        self.pool.add(proxy)
            except Exception as e:
                print(e)
                print("爬虫",spider,"出现错误")


    def run(self):
        self.process_proxy_spiders()

if __name__ == '__main__':
    spider = ProxySpider()
    spider.run()