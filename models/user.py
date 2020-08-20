import uuid

__author__ = 'Robert W. Curtiss'
__project__ = 'NutFlask'
import common.globals

from flask import make_response, jsonify
from flask.views import MethodView
from flask_restful import reqparse
from common.database import Database
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
class User(MethodView):
    def __init__(self,username,password, _id=None):
        self._id = uuid.uuid4().hex if _id is None else _id
        self.username = username
        self.password = password

    @classmethod
    def get_by_username(cls, username):
        data = Database.find_one("Users", {'name': username})
        if data:
            return cls(**data)

    def save_to_mongo(self):
        Database.insert("Users", self.json())

    @classmethod
    def find_by_id(cls,id):
        data = Datatbase.find_one("Users", {'_id' : id})
        if data:
            return cls(**data)

    def json(self):
        return {
            '_id': self._id,
            'username': self.username,
            'password': self.password
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
        if User.find_by_username(data['username']):
            return make_response(jsonify({'message' : 'A user with that name already exists!'}),400)
        save_to_mongo()
        # connection = sqlite3.connect(SQLITE_DB)
        # cursor = connection.cursor()
        #
        # query = "INSERT INTO users VALUES (NULL, ?,?)"
        # cursor.execute(query,(data['username'],data['password']))
        # connection.commit()
        # connection.close()
        return make_response( jsonify({"message" :"User Created Successfully "},201))



