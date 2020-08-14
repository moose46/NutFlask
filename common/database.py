__author__ = 'Robert W. Curtiss'
__project__ = ''

"""
====================================================
Author: Robert W. Curtiss
    Project: 
    File: database
    Created: Jul, 27, 2020
    
    Description:
    
===================================================
"""

import pymongo

class Database (object):
    uri = "mongodb://localhost:27017"
    test_uri = "mongodb://localhost:27017"
    DATABASE = None
    @staticmethod
    def initialize(test=False):
        if test == False:
            client = pymongo.MongoClient(Database.uri)
            Database.DATABASE = client['NutFlask']
        else:
            client = pymongo.MongoClient(Database.test_uri)
            Database.DATABASE = client['NutFlask']

    @staticmethod
    def insert(collection, data):
        try:
            return Database.DATABASE[collection].insert_one(data)
        except Exception as e:
            return e

    @staticmethod
    def find(collection, query):
        return Database.DATABASE[collection].find(query)

    @staticmethod
    def find_one(collection, query):
        try:
            x = Database.DATABASE[collection].find_one(query)
            return x
        except Exception as e:
            return e
    @staticmethod
    def delete_one(collection, query):
        return Database.DATABASE[collection].delete_one(query)

    @staticmethod
    def get_list(collection):
        return Database.DATABASE[collection].find()

    @staticmethod
    def update(collection,mongo_id, new_values):
        new_value = {"$set" : new_values}
        try:
            return True,Database.DATABASE[collection].update_one({'_id' : mongo_id}, new_value)
        except Exception as e:
            return False, e
