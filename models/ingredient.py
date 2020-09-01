__author__ = 'Robert W. Curtiss'
__project__ = 'Breathing Air Solutions'

import datetime

from flask import Flask, request, make_response, jsonify, redirect, url_for
from flask.views import MethodView
from flask_restful import reqparse, Api

from common.globals import SQLITE_DB
from models.measurement import MeasurementBase
from models.nutflaskbase import NutFlaskBase

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


# https://www.udemy.com/course/rest-api-flask-and-python/learn/lecture/5960152#overview
class Ingredient(MethodView, NutFlaskBase):
    parser = reqparse.RequestParser()
    parser.add_argument('name',
                        required=True,
                        help={'message', 'This Field cannot be left blank!'})
    parser.add_argument('usage',
                        required=True,
                        help={'message', 'This Field can be left blank!'})
    parser.add_argument('side_effects',
                        required=True,
                        help={'message', 'This Field can be left blank!'})

    def __init__(self, name='n/a', usage='N/A', _id=None, side_effects="None",
                 date_created=None,date_updated=None):
        super().__init__()

        self.name = name
        self.usage = usage
        self._id = uuid.uuid4().hex if _id is None else _id
        self.side_effects = side_effects


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
            'side_effects': self.side_effects,
            'date_created': self.date_created,
            "date_updated": self.date_updated
        }
    def json_update(self):
        return {
            'name': self.name,
            'usage': self.usage,
            'side_effects': self.side_effects,
            'date_created': self.date_created,
            "date_updated": self.date_updated
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

    # @jwt_required()
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
            return {"error": e}

    def post(self, name):
        body = Ingredient.parser.parse_args()
        x = Ingredient.get_by_name(name)
        if x:
            return make_response(jsonify(self.error["itemAlreadyExists"]), 400)
        self.name = name
        results = self.save_to_mongo()
        return make_response(self.json(), 201)

    # update product name
    def put(self):
        body = Ingredient.parser.parse_args()
        update_ingredient = Ingredient(name=body['name'], usage=body['usage'], side_effects=body['side_effects'])
        old_data = Ingredient.get_by_name(update_ingredient.name)
        if old_data is None:
            return make_response(jsonify(self.error["itemNotFound"]), 400)
        #old_obj = self.get_by_name(update_ingredient.name)
        update_ingredient.date_created = old_data.date_created #preserve orginal date created
        results = Ingredient.update(mongo_id=old_data._id, new_value=update_ingredient.json_update())
        if results[0] == True:
            return make_response(jsonify(update_ingredient.json()), 200)
        else:
            return make_response(jsonify(results[1].details), 400)

    def delete(self, name):
        """ Delete an item """
        x = Ingredient.get_by_name(name)
        if x is None:
            return make_response(jsonify(self.error["itemNotFound"]), 400)
        self.delete_by_name(name)
        return make_response(jsonify({}), 200)
