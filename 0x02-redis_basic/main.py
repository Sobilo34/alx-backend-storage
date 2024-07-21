#!/usr/bin/env python3
""" Main file """
from exercise import Cache, replay

Cache = __import__('exercise').Cache

cache = Cache()

s1 = cache.store("foo")
print(s1)
s2 = cache.store("bar")
print(s2)
s3 = cache.store(43)
print(s3)

inputs = cache._redis.lrange("{}:inputs".format(cache.store.__qualname__), 0, -1)
outputs = cache._redis.lrange("{}:outputs".format(cache.store.__qualname__), 0, -1)

print("inputs: {}".format(inputs))
print("outputs: {}".format(outputs))

replay(cache.store)
