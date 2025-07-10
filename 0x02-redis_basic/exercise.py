#!/usr/bin/env python3
import redis
import uuid

class Cache:
    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb()
    def store(self,data):
          _uuid = uuid.uuid4()
          self._redis.set(str(_uuid),data)
          return str(_uuid)
        

