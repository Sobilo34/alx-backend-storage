#!/usr/bin/env python3
"""
A Python function that lists all documents in a collection
"""


def list_all(mongo_collection):
    """
    lists all documents
    """
    list_of_docs = []

    for doc in mongo_collection.find():
        if doc:
            list_of_docs.append(doc)
    return list_of_docs
