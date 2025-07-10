#!/usr/bin/env python3
"""
A module for caching data in Redis.
"""
from functools import wraps 
import redis
import uuid
from typing import Union,Callable,Optional

def count_calls(method:Callable) -> Callable:
    @wraps(method)
    def wrapper(self,*args,**kwargs):
        key = method.__qualname__
        self._redis.incr(key)
        return method(self,*args,**kwargs)
    return wrapper

def call_history(method:Callable) -> Callable:
    @wraps(method)
    def wrapper(self,*args,**kwargs):
        name = method.__qualname__
        self._redis.rpush(name+":inputs",str(args))
        output = method(self,*args,**kwargs)
        self._redis.rpush(name+":outputs",output)
        return output
    return wrapper

def replay(method: Callable):
    r = redis.Redis()
    name = method.__qualname__
    
    inputs = r.lrange(f"{name}:inputs", 0, -1)
    outputs = r.lrange(f"{name}:outputs", 0, -1)

    print(f"{name} was called {r.get(name).decode('utf-8')} times:")

    for i, o in zip(inputs, outputs):
        print(f"{name}(*{i.decode('utf-8')}) -> {o.decode('utf-8')}")


class Cache:
    def __init__(self) -> None:
        self._redis = redis.Redis()
        self._redis.flushdb()
    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key
    def get(self,key:str,fn:Optional[Callable]=None) -> Union[str,bytes,int,float,None]:
        data = self._redis.get(key)
        if data is None:
            return None
        if fn is not None:
            return fn(data)
        return data
    def get_str(self,key:str) -> Union[str,None]:
        return self.get(key,fn=lambda d: d.decode("utf-8"))
    def get_int(self,key:str) -> Union[int,None]:
        return self.get(key,fn=int)



