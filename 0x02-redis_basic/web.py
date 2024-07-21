#!/usr/bin/env python3
"""
Module for caching and counting web page requests using Redis.

This module defines a decorator to count the number of times a URL is requested
and to cache the HTML content of the URL for a specified period of time.
"""

import redis
import requests
from functools import wraps

r = redis.Redis()


def url_access_count(method):
    """
    Decorator to cache the HTML content of a URL and count access requests.

    Args:
        method (Callable): The method to decorate.

    Returns:
        Callable: The decorated method.
    """
    @wraps(method)
    def wrapper(url):
        """
        Wrapper function for caching and counting URL access.

        Args:
            url (str): The URL to request.

        Returns:
            str: The HTML content of the URL.
        """
        key = "cached:" + url
        cached_value = r.get(key)
        if cached_value:
            return cached_value.decode("utf-8")

        # Get new content and update cache
        key_count = "count:" + url
        html_content = method(url)

        r.incr(key_count)
        r.set(key, html_content, ex=10)
        return html_content

    return wrapper


@url_access_count
def get_page(url: str) -> str:
    """
    Obtain the HTML content of a particular URL.

    Args:
        url (str): The URL to request.

    Returns:
        str: The HTML content of the URL.
    """
    response = requests.get(url)
    return response.text


if __name__ == "__main__":
    import doctest
    doctest.testmod()

    # Example usage
    url = 'http://slowwly.robertomurray.co.uk'
    print(get_page(url))
    print(get_page(url))  # This call should hit the cache
