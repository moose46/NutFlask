__author__ = 'Robert W. Curtiss'
__project__ = 'Breathing Air Solutions'

from flask import Flask, request, make_response,jsonify,redirect,url_for
from flask.views  import MethodView
from flask_restful import reqparse,Api

from common.globals import SQLITE_DB

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


import uuid

from common.database import Database
from flask_jwt import jwt_required
import sqlite3

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
class Ingredient(MethodView):
    parser = reqparse.RequestParser()
    parser.add_argument('name',
                        required=True,
                        help={'message', 'This Field cannot be left blank!'})
    parser.add_argument('usage',
                        required=False,
                        help={'message', 'This Field can be left blank!'})
    parser.add_argument('side_effects',
                        required=False,
                        help={'message', 'This Field can be left blank!'})

    def __init__(self, name='n/a', usage='N/A', _id=None, side_effects = "None"):

        self.name = name
        self.usage = usage
        self._id = uuid.uuid4().hex if _id is None else _id
        self.side_effects = side_effects
    def save_to_sqlLite(self):
        data = Ingredient.parser.parse_args()

        connection = sqlite3.connect(SQLITE_DB)
        cursor = connection.cursor()
        query = "INSERT INTO ingredient (NULL,?,?,?)"
        cursor.execute(query,(data['name'],data['usage'], data['side_effects']))

        connection.commit()
        connection.close()
        return make_response( jsonify({"message" :"Ingredient Created Successfully "},201))

    def save_to_mongo(self):
        Database.insert("Ingredient", self.json())


    def get_by_id(self, id):
        return Database.find_one("Ingredient", {'_id': id})
    @classmethod
    def get_by_name(cls, ingredient_name):
        data = Database.find_one("Ingredient", {'name': ingredient_name})
        if data is not None:
            return cls(**data)

    @classmethod
    def delete_by_name(cls, ingredient_name):
        return Database.delete_one("Ingredient", {'name': ingredient_name})
    @classmethod
    def get_list(cls):
        return Database.get_list("Ingredient")


    @classmethod
    def update(cls, mongo_id, new_value):
        return Database.update("Ingredient", mongo_id=mongo_id, new_values=new_value)

    def json(self):
        return {
            '_id': self._id,
            'name': self.name,
            'usage': self.usage,
            'side_effects' : self.side_effects
        }
    """
    https://www.udemy.com/course/rest-api-flask-and-python/learn/lecture/5960156#overview
    """
    error = {
        "itemNotFound": {
            "errorCode": "itemNotFound",
            "errorMessage": "Item not found"
        },
        "itemAlreadyExists": {
            "errorCode": "itemAlreadyExists",
            "errorMessage": "Could not create item. Item already exists"
        }
    }
    #@jwt_required()
    def get(self, name):

        try:
            x = Ingredient.get_by_name(name)
            if x is not None:
                return make_response(x.json(), 200)
            elif name is None:
                # just return a list of ingredients if there was no argument
                l1 = list(Database.get_list('Ingredient'))
                return make_response(jsonify(l1, 200))
            else:
                return make_response(jsonify(self.error["itemNotFound"]), 400)

        except Exception as e:
            return {"error" : e}
    def post(self,name):
        body = Ingredient.parser.parse_args()
        x = Ingredient.get_by_name(name)
        if x:
            return make_response(jsonify(self.error["itemAlreadyExists"]), 400)
        self.name = name
        results = self.save_to_mongo()
        return make_response(self.json(),201)

    def put(self,name):
        body = Ingredient.parser.parse_args()
        new_name = body['name']
        old_data = Ingredient.get_by_name(name)
        if old_data is None:
            return make_response(jsonify(self.error["itemNotFound"]), 400)
        old_obj = self.get_by_name(name)
        results = Ingredient.update(mongo_id=old_obj._id, new_value=body)
        if results[0] == True:
            return make_response(jsonify(body),200)
        else:
            return make_response(jsonify(results[1].details),400)

    def delete(self, name):
        """ Delete an item """
        x = Ingredient.get_by_name(name)
        if x is None:
            return make_response(jsonify(self.error["itemNotFound"]), 400)
        self.delete_by_name(name)
        return make_response(jsonify({}), 200)

