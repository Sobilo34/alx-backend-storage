#!/usr/bin/env python3
"""
A Python function that returns the list of schools having a specific topic
"""

def schools_by_topic(mongo_collection, topic):
    """
    Returns the list of schools having a specific topic.

    Args:
    mongo_collection (pymongo.collection.Collection): The MongoDB collection.
    topic (str): The topic to search for.

    Returns:
    list: A list of schools that have the specific topic.
    """
    # Assuming the field name in the MongoDB documents is 'topics'
    return list(mongo_collection.find({"topics": topic}))

