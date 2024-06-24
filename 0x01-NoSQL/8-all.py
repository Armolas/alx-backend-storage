#!/usr/bin/env python3
""" lists all documents in a collection"""


def list_all(mongo_collection):
    """lists all docs in the collection"""
    if mongo_collection.estimated_document_count() == 0:
        return []
    return mongo_collection.find()
