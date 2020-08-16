__author__ = 'Robert W. Curtiss'
__project__ = 'NutFlask'
import sqlite3,common.globals

from flask import make_response, jsonify
from flask.views import MethodView
from flask_restful import reqparse

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
class User:
    def __init__(self,id,username,password):
        self.id = id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls,username):
        connection = sqlite3.connect(SQLITE_DB)
        cursor = connection.cursor()

        query = "SELECT * from users WHERE username=?"
        result = cursor.execute(query,(username,))
        row = result.fetchone()
        if row:
            user = cls(*row)
        else:
            user = None
        connection.close()
        return user

    @classmethod
    def find_by_id(cls,id):
        connection = sqlite3.connect(SQLITE_DB)
        cursor = connection.cursor()
        query = "SELECT * from users WHERE id=?"
        result = cursor.execute(query,(id,))
        row = result.fetchone()
        if row:
            user = cls(*row)
        else:
            user = None
        connection.close()
        return user

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

        connection = sqlite3.connect(SQLITE_DB)
        cursor = connection.cursor()

        query = "INSERT INTO users VALUES (NULL, ?,?)"
        cursor.execute(query,(data['username'],data['password']))
        connection.commit()
        connection.close()
        return make_response( jsonify("User Created Successfully ",201))



