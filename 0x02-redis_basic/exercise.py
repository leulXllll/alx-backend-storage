#!/usr/bin/env python3
"""
A module for caching data in Redis.
"""
import redis
import uuid
from typing import Union,Callable,Optional


class Cache:
    def __init__(self) -> None:
        self._redis = redis.Redis()
        self._redis.flushdb()

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



