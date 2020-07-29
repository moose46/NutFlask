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
        Database.DATABASE[collection].insert_one(data)

    @staticmethod
    def find(collection, query):
        return Database.DATABASE[collection].find(query)

    @staticmethod
    def find_one(collection, query):
        return Database.DATABASE[collection].find_one(query)

    @staticmethod
    def delete_one(collection, query):
        return Database.DATABASE[collection].delete_one(query)

    @staticmethod
    def get_list(collection):
        return Database.DATABASE[collection].find()
