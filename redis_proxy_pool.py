#!/usr/bin/python3
# -*- coding: utf-8 -*-


import settings
import redis
from random import choice

MAX_SCORE = 100
MIN_SCORE = 0
INITIAL_SCORE = 10

class RedisProxyPool(object):

    def __init__(self,host=settings.REDIS_HOST,port=settings.REDIS_PORT):
        self.db = redis.StrictRedis(host=host,port=port,decode_responses=True)


    def add(self, proxy, score=INITIAL_SCORE):
        '''
        添加一个代理到代理池中
        :param proxy: 代理
        :param score: 分数
        :return: 
        '''
        if not self.db.zscore(settings.PROXIES_REDIS_KEY,proxy):
            return self.db.zadd(settings.PROXIES_REDIS_KEY,score,proxy)

    def random(self):
        '''
        随机一个代理
        获取最高分的代理，
        如果没有最高分就获取
        :return: 
        '''

        result = self.db.zrangebyscore(settings.PROXIES_REDIS_KEY,MAX_SCORE,MAX_SCORE)
        if len(result):
            return choice(result)
        else:
            result = self.db.zrevrange(settings.PROXIES_REDIS_KEY,MIN_SCORE,MAX_SCORE)
            if len(result):
                return choice(result)
            else:
                raise Exception("PoolEmptyError")

        pass

    def decrease(self, proxy):
        '''
        降低代理分数，如果代理小于最小值，则代理删除

        :param proxy: 代理
        :return: 
        '''
        score = self.db.zscore(settings.PROXIES_REDIS_KEY,proxy)
        if score and score > MIN_SCORE:
            print("代理",proxy,"当前分数",score,'减 1')
            return self.db.zincrby(settings.PROXIES_REDIS_KEY,proxy,-1)
        else:
            print("代理",proxy,"当前分数",score,'移除')
            return self.db.zrem(settings.PROXIES_REDIS_KEY,proxy)

    def exists(self, proxy):
        '''
        是否存在代理
        :param proxy: 代理
        :return: 
        '''
        return not self.db.zscore(settings.REDIS_HOST,proxy) == None

    def max(self, proxy):
        '''
        将代理设置成最大分数
        :param proxy: 代理
        :return: 
        '''
        print("代理",proxy,"可用。 设置为",MAX_SCORE)
        return self.db.zadd(settings.PROXIES_REDIS_KEY,MAX_SCORE,proxy)

    def count(self):
        '''
        获取代理最大数量
        :return: 
        '''
        return self.db.zcard(settings.PROXIES_REDIS_KEY)

    def all(self):
        '''
        获取所有的代理
        :return: 
        '''
        return self.db.zrangebyscore(settings.PROXIES_REDIS_KEY,MIN_SCORE,MAX_SCORE)