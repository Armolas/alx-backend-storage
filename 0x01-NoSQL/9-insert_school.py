#!/usr/bin/env python3
"""inserts a new school"""


def insert_school(mongo_collection, **kwargs):
    """inserts a new school to collection"""
    return mongo_collection.insert_one(kwargs).inserted_id
