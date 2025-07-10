#!/usr/bin/env python3
"""
A module for caching data in Redis.
"""
import redis
import uuid
from typing import Union


class Cache:
    """
    A class for caching data in Redis.
    """
    def __init__(self) -> None:
        """
        Initializes the Cache object and flushes the Redis database.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Stores data in Redis with a random key and returns the key.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key