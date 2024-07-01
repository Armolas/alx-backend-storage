#!/usr/bin/env python3
'''exercise task'''
from functools import wraps
import redis
import uuid
from typing import Union, Callable, Any


def count_calls(method: Callable) -> Callable:
    '''counts how many times the Cache class is called'''
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        '''counts calls'''
        key = f"{method.__qualname__}"
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper
class Cache:
    '''This is a redis Cache class'''
    def __init__(self):
        '''initializes a redis instance and flushed the db'''
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        '''stores a data in redis'''
        key = str(uuid.uuid1())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Callable = None) -> Union[str, bytes, int, float]:
        '''convert data to desired format'''
        value = self._redis.get(key)
        if value is not None and fn is not None:
            value = fn(value)
        return value

    def get_str(self, key: str) -> Union[str, None]:
        '''converts data to string'''
        value = self._redis.get(key)
        if value is not None:
            value = str(value)
        return value

    def get_int(self, key: str) -> Union[int, None]:
        '''converts data to an integer'''
        value = self._redis.get(key)
        if value is not None and isNaN(value) is False:
            value = int(value)
        return value
