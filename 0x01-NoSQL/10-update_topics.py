#!/usr/bin/env python3
"""updates topics"""


def update_topics(mongo_collection, name, topics):
    """updates the topics of a collection"""
    mongo_collection.update_one(
            {"name": name},
            {"$set": {"topics": topics}}
        )
