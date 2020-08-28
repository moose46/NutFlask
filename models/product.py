__author__ = 'Robert W. Curtiss'
__project__ = 'NutFlask'

import uuid

from flask import make_response, jsonify, request
from flask.views import MethodView
from flask_restful import reqparse

from common.database import Database
from models.ingredient import Ingredient
from models.user import UserRegister

"""
====================================================
Author: Robert W. Curtiss
    Project: NutFlask
    File: product
    Created: Aug, 24, 2020
    
    Description:
    
===================================================
"""


class ProductParams(MethodView):

    parser = reqparse.RequestParser()
    parser.add_argument('product_name',
        required=True,
        help={'message', 'Product Name Field cannot be left blank!'})
    parser.add_argument('ingredients', type=list,
        required=False,
        help={'message', 'Ingredients Field cannot be left blank!'})


class Product(MethodView):
    #todo: add date created and date updated
    def __init__(self, product_name="None", ingredients=None, _id = None):
        self.product_name = product_name
        self.ingredients = ingredients
        self._id = uuid.uuid4().hex if _id is None else _id

    # @property
    # def ingredients_list(self):
    #     return self.ingredients
    #
    # @ingredients_list.setter
    # def ingredients_list(self,value):
    #     self.ingredients.append(value)

    def save_to_mongo(self):
        Database.insert("Products", self.json)
    @classmethod
    def get_list(cls):
        return Database.get_list("Products")
    @classmethod
    def get_by_product_name(cls, product_name):
        data = Database.find_one("Products", {'product_name': product_name})
        if data:
            return cls(**data)
    @classmethod
    def update(cls, mongo_id, new_value):
        return Database.update("Products", mongo_id=mongo_id, new_values=new_value)

    def find_by_id(cls, id):
        data = Database.find_one("Products", {'_id': id})
        if data:
            return cls(**data)

    @property
    def json(self):
        return {
            "_id" : self._id,
            'product_name' : self.product_name,
            'ingredients' : self.ingredients
        }
    def get(self,name=None):

        try:
            if name:
                x = Product.get_by_product_name(name)
                return make_response(jsonify(x.json), 200)
            elif name is None:
                # just return a list of ingredients if there was no argument
                l1 = list(Database.get_list('Products'))
                return make_response(jsonify(l1, 200))
            else:
                return make_response(jsonify(self.error["itemNotFound"]), 400)
        except Exception as e:
            return {"error": e}

    def post(self):
        payload = request.json
        data = ProductParams.parser.parse_args()
        product = Product.get_by_product_name(data['product_name'])
        if product:
            return make_response(jsonify({'message' : 'A product with that name already exists!'}),400)
        for i in payload['ingredients']:
            new_i = Ingredient.get_by_name(i)
            if new_i:
                self.ingredients.append(new_i.name)
            else:
                new_i = Ingredient(name=i)
                new_i.save_to_mongo()
                self.ingredients.append(new_i.name)

        product = Product(product_name=data['product_name'])
        product.ingredients = self.ingredients
        product.save_to_mongo()
        return make_response( jsonify({"message" :"Product Created Successfully "},201))
