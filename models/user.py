import uuid

__author__ = 'Robert W. Curtiss'
__project__ = 'NutFlask'
import common.globals
import datetime

from flask import make_response, jsonify
from flask.views import MethodView
from flask_restful import reqparse
from common.database import Database
from models.nutflaskbase import NutFlaskBase

"""
====================================================
Author: Robert W. Curtiss
    Project: Ingredient
    File: user
    Created: Aug, 12, 2020
    
    Description:
    https://www.udemy.com/course/rest-api-flask-and-python/learn/lecture/5965500#overview
===================================================
"""
from common.globals import SQLITE_DB
class User(MethodView, NutFlaskBase):
    def __init__(self,username,password, _id=None, date_created=None,date_updated=None):
        self.id = uuid.uuid4().hex if _id is None else _id
        self.username = username
        self.password = password
        super().__init__()
    @classmethod
    def get_by_username(cls, username):
        data = Database.find_one("Users", {'username': username})
        if data:
            return cls(**data)

    def save_to_mongo(self):
        Database.insert("Users", self.json())

    @classmethod
    def find_by_id(cls,id):
        data = Database.find_one("Users", {'_id' : id})
        if data:
            return cls(**data)
    @classmethod
    def delete_by_username(cls, username):
        return Database.delete_one("Users", {'username': username})
    @classmethod
    def get_list(cls):
        return Database.get_list("Users")

    @classmethod
    def update(cls, mongo_id, new_value):
        return Database.update("Users", mongo_id=mongo_id, new_values=new_value)
    def json(self):
        return {
            '_id': self.id,
            'username': self.username,
            'password': self.password,
            'date_created' : self.date_created,
            'date_updated' : self.date_updated
        }

class UserRegister(MethodView):

    parser = reqparse.RequestParser()
    parser.add_argument('username',
        required=True,
        help={'message', 'UserName Field cannot be left blank!'})
    parser.add_argument('password',
        required=True,
        help={'message', 'Password Field cannot be left blank!'})


    def post(self):
        data = UserRegister.parser.parse_args()
        user = User.get_by_username(data['username'])
        if user:
            return make_response(jsonify({'message' : 'A user with that name already exists!'}),400)
        user = User(data['username'],data['password'])
        user.save_to_mongo()
        return make_response( jsonify({"message" :"User Created Successfully "},201))

    def delete(self):
        data = UserRegister.parser.parse_args()
        user = User.get_by_username(data['username'])
        if user == None:
            return make_response(jsonify({'message' : 'A user with that name does not exist exist!'}),400)
        user = User(data['username'],data['password'])
        user.delete_by_username(data['username'])
        return make_response( jsonify({"message" :"User Deleted Successfully "},201))

    def put(self):
        data = UserRegister.parser.parse_args()
        user = User.get_by_username(data['username'])
        if user == None:
            return make_response(jsonify({'message' : 'A user with that name does not exist exist!'}),400)
        if len(data['password']) > 4:
            user.update(user.id, {'password': data['password']})
        return make_response(jsonify({'message' : 'Password updated!'}),200)



