#!/usr/bin/env python3
"""
Implementation of Cache class to handle basic caching operations
using Redis as the backend storage. Supports storing and retrieving
data with custom conversion functions.
"""
import redis
from uuid import uuid4
from typing import Callable, Optional, Union
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """
    Decorator to count the number of calls to a method.

    Args:
        method (Callable): The method to decorate.

    Returns:
        Callable: The decorated method.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """
    Decorator to store the history of inputs and outputs for a method.

    Args:
        method (Callable): The method to decorate.

    Returns:
        Callable: The decorated method.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        method_name = method.__qualname__
        self._redis.rpush(method_name + ":inputs", str(args))
        output = method(self, *args, **kwargs)
        self._redis.rpush(method_name + ":outputs", str(output))
        return output
    return wrapper


def replay(method: Callable) -> None:
    """
    Displays the history of calls to a method.

    Args:
        method (Callable): The method to replay.
    """
    method_name = method.__qualname__
    redis_client = method.__self__._redis
    inputs = redis_client.lrange(method_name + ":inputs", 0, -1)
    outputs = redis_client.lrange(method_name + ":outputs", 0, -1)

    print(f"{method_name} was called {len(inputs)} times:")
    for input_data, output_data in zip(inputs, outputs):
        input_data = input_data.decode("utf-8")
        output_data = output_data.decode("utf-8")
        print(f"{method_name}(*{eval(input_data)}) -> {output_data}")


class Cache:
    """
    Cache class to interact with Redis.
    """

    def __init__(self):
        """
        Initialize the Cache class with a Redis connection.
        """
        self._redis = redis.Redis(host='localhost', port=6379, db=0)
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data) -> str:
        """
        Store data in Redis and return a unique key.

        Args:
            data (str): The data to store.

        Returns:
            str: The unique key for the stored data.
        """
        key = str(uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable] = None
            ) -> Union[bytes, float, str, int, None]:
        """
        Retrieve data from Redis by key.

        Args:
            key (str): The key of the data.
            fn (Optional[Callable]): A function to transform the data.

        Returns:
            Union[bytes, float, str, int, None]: The retrieved data.
        """
        data = self._redis.get(key)
        if data is not None and fn is not None:
            data = fn(data)
        return data

    def get_str(self, key: str) -> Union[str, None]:
        """
        Retrieve data from Redis and decode it as a string.

        Args:
            key (str): The key of the data.

        Returns:
            Union[str, None]: The decoded data.
        """
        return self.get(key, lambda x: x.decode('utf-8'))

    def get_int(self, key: int) -> Union[int, None]:
        """
        Retrieve data from Redis and convert it to an integer.

        Args:
            key (int): The key of the data.

        Returns:
            Union[int, None]: The integer value.
        """
        return self.get(key, int)
