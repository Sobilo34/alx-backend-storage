#!/usr/bin/env python3
"""
A Python function that inserts a new document in a collection based on kwargs
"""


def insert_school(mongo_collection, **kwargs):
    """
    insert schools
    """ 
    new_docs = mongo_collection.insert_one(kwargs)
    return new_docs.inserted_id
