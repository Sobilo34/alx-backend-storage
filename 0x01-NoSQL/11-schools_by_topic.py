#!/usr/bin/env python3
"""
A Python function that returns the list of school having a specific topic
"""


def schools_by_topic(mongo_collection, topic):
    """
    returns the list of school
    """
    new_schools = []
    school = mongo_collection.find({ "topic" : topic })
    for sch in school:
        new_schools.append(sch)

    return new_schools
