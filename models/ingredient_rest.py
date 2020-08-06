__author__ = 'Robert W. Curtiss'
__project__ = 'Breathing Air Solutions'

from flask.views import MethodView

"""
====================================================
Author: Robert W. Curtiss
    Project: Breathing Air Solutions
    File: ingredient_rest
    Created: Jul, 30, 2020
    
    Description:
    
===================================================
"""
__author__ = 'Robert W. Curtiss'
__project__ = 'Breathing Air Solutions'

import uuid
from importlib.resources import Resource

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

#https://www.udemy.com/course/rest-api-flask-and-python/learn/lecture/5960152#overview
class Ingredient_rest(MethodView):
    def __init__(self, name='n/a', usage='N/A', _id=None):

         self.name = name
         self.usage = usage
         self._id = uuid.uuid4().hex if _id is None else _id

    def save_to_mongo(self):
        Database.insert("Ingredient", self.json())

    # @classmethod
    # def find(self):
    #     '''use class method to return the object'''
    #     ingredient_list = Database.find("Ingredient", None)
    #     return ingredient_list

    def get_by_id(self, id):
        return Database.find_one("Ingredient", {'_id': id})
    @classmethod
    def get_by_name(cls, ingredient_name):
        return Database.find_one("Ingredient", {'name': ingredient_name})

    def delete_by_name(self, ingredient_name):
        return Database.delete_one("Ingredient", {'name': ingredient_name})

    def json(self):
        return {
            '_id': self._id,
            'name': self.name,
            'usage': self.usage
        }
    # def post(self, name, usage):
    #     self.name = name
    #     self.usage = usage
    #     return self
    # def get(self):
    #     return self.Database.find("Ingredient", None)
    """
    https://www.udemy.com/course/rest-api-flask-and-python/learn/lecture/5960156#overview
    """
    @classmethod
    def get(cls, name):
        try:
            x = Ingredient_rest.get_by_name(name)
            if x is not None:
                return x

            return{"ingredient" : None}, 404
        except Exception as e:
            return {"error" : e}
    def post(self, name):
        print(name)
        self.name = name
        self.save_to_mongo()
        return self.json()