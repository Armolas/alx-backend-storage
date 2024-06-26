#!/usr/bin/env python3
'''exercise task'''
from functools import wraps
import redis
import uuid
from typing import Union, Callable, Any


def call_history(method: Callable) -> Callable:
    '''store history of inputs'''
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        input_key = f"{method.__qualname__}:inputs"
        output_key = f"{method.__qualname__}:outputs"
        self._redis.rpush(input_key, str(args))
        output = method(self, *args,**kwargs)
        self._redis.rpush(output_key, output)
        return output
    return wrapper

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

    @call_history
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

def replay(method: Callable) -> None:
    redis_client = method.__self__._redis
    calls_key = f"{method.__qualname__}:calls"
    inputs_key = f"{method.__qualname__}:inputs"
    outputs_key = f"{method.__qualname__}:outputs"

    num_calls = redis_client.get(calls_key)
    if num_calls is None:
        print(f"{method.__qualname__} was never called.")
        return

    num_calls = int(num_calls)
    print(f"{method.__qualname__} was called {num_calls} times:")

    inputs = redis_client.lrange(inputs_key, 0, -1)
    outputs = redis_client.lrange(outputs_key, 0, -1)

    for input_args, output in zip(inputs, outputs):
        print(f"{method.__qualname__}(*{input_args.decode('utf-8')}) -> {output.decode('utf-8')}")
