#!/usr/bin/env python3
import pymongo


def connect_to_mongodb(database_name):
    """
    Connect to MongoDB and return the client and collection objects.

    Args:
    - database_name (str): The name of the MongoDB database.

    Returns:
    - pymongo.MongoClient: MongoDB client object.
    - pymongo.collection.Collection: MongoDB collection object.
    """
    try:
        client = pymongo.MongoClient()
        db = client[database_name]
        collection = db['nginx']
        return client, collection
    except pymongo.errors.ConnectionFailure as e:
        print(f"Error connecting to MongoDB: {e}")
        return None, None


def count_documents(collection):
    """
    Count the total number of documents in the collection.

    Args:
    - collection (pymongo.collection.Collection): MongoDB collection object.

    Returns:
    - int: Number of documents in the collection.
    """
    return collection.count_documents({})


def count_methods(collection):
    """
    Count occurrences of each HTTP method in the collection.

    Args:
    - collection (pymongo.collection.Collection): MongoDB collection object.

    Returns:
    - dict: Dictionary containing counts for each HTTP method.
    """
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    method_counts = {}
    for method in methods:
        count = collection.count_documents({"method": method})
        method_counts[method] = count
    return method_counts


def count_status_check(collection):
    """
    Count documents where method=GET and path=/status.

    Args:
    - collection (pymongo.collection.Collection): MongoDB collection object.

    Returns:
    - int: Number of documents with method=GET and path=/status.
    """
    return collection.count_documents({"method": "GET", "path": "/status"})


if __name__ == "__main__":
    # Connect to MongoDB and select the 'logs' database
    client, collection = connect_to_mongodb('logs')
 
    if collection:
        # Count total number of logs
        total_logs = count_documents(collection)
        print(f"{total_logs} logs")

        # Count methods
        method_counts = count_methods(collection)
        print("Methods:")
        for method, count in method_counts.items():
            print(f"    method {method}: {count}")

        # Count status check
        status_check_count = count_status_check(collection)
        print(f"{status_check_count} status check")

        # Close MongoDB connection
        client.close()
    else:
        print("MongoDB connection error, check your connection settings.")
