__author__ = 'Robert W. Curtiss'
__project__ = 'NutFlask'

from flask import make_response, jsonify
from flask.views import MethodView
from flask_restful import reqparse

from common.database import Database
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
    # parser.add_argument('password',
    #     required=True,
    #     help={'message', 'Password Field cannot be left blank!'})


class Product(MethodView):
    def __init__(self, product_name="None"):
        self.product_name = product_name

    def save_to_mongo(self):
        Database.insert("Products", self.json())
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

    def json(self):
        return {
            'product_name' : self.product_name
        }

    def post(self):
        data = ProductParams.parser.parse_args()
        product = Product.get_by_product_name(data['product_name'])
        if product:
            return make_response(jsonify({'message' : 'A product with that name already exists!'}),400)
        product = Product(data['product_name'])
        product.save_to_mongo()
        return make_response( jsonify({"message" :"Product Created Successfully "},201))
