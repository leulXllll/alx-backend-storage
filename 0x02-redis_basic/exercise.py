#!/usr/bin/env python3
import redis
import uuid
from typing import Union

class Cache:
    def __init__(self)->None:
        self._redis = redis.Redis()
        self._redis.flushdb()
    def store(self,data: Union[str,bytes,int,float])-> str:
          _uuid = uuid.uuid4()
          self._redis.set(str(_uuid),data)
          return str(_uuid)
        

