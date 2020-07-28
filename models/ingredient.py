__author__ = 'Robert W. Curtiss'
__project__ = 'Breathing Air Solutions'

import uuid

from common.database import Database

"""
====================================================
Author: Robert W. Curtiss
    Project: Breathing Air Solutions
    File: ingredient
    Created: Jul, 27, 2020
    
    Description:
    
===================================================
"""
class Ingredient(object):
    def __init__(self, name, usage = 'N/A', _id=None):
        self.name = name
        self.usage = usage
        self._id = uuid.uuid4().hex if _id is None else _id

    def save_to_mongo(self):
        Database.insert("Ingredient", self.json())

    @classmethod
    def get_by_id(cls, id):
        return cls(**Database.find_one("Ingredient", {'_id': id}))

    @classmethod
    def get_by_name(cls, ingredient_name):
        return cls(**Database.find_one("Ingredient", {'name': ingredient_name}))

    @classmethod
    def delete_by_name(cls, ingredient_name):
        return cls(Database.delete_one("Ingredient", {'name' : ingredient_name}))

    def json(self):
        return {
        '_id': self._id,
        'name': self.name,
        'usage': self.usage
        }