#!/usr/bin/env python3
'''exercise task'''
import redis
import uuid
from typing import Union


class Cache:
    '''This is a redis Cache class'''
    def __init__(self):
        '''initializes a redis instance and flushed the db'''
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        '''stores a data in redis'''
        key = str(uuid.uuid1())
        self._redis.set(key, data)
        return key
