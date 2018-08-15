#!/usr/bin/python3
# -*- coding: utf-8 -*-

from flask import Flask
from redis_proxy_pool import RedisProxyPool
import json

class ProxyProvider(object):
    def __init__(self):
        self.app = Flask(__name__)
        self.proxyPool = RedisProxyPool()

        @self.app.route('/proxies')
        def all():
            return json.dumps(self.proxyPool.all())

        @self.app.route('/proxies/random')
        def random():
            return self.proxyPool.random()

    def run(self):
        self.app.run(host="0.0.0.0",port=6868)

if __name__ == '__main__':
    proxyProvider = ProxyProvider()
    proxyProvider.run()