#!/usr/bin/env python3
"""find school"""


def schools_by_topic(mongo_collection, topic):
    """finds a school by topic"""
    # Query MongoDB for schools with the specified topic
    cursor = mongo_collection.find({"topics": topic})

    # Convert cursor to a list of dictionaries
    schools_list = list(cursor)

    return schools_list
