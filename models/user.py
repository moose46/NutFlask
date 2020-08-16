__author__ = 'Robert W. Curtiss'
__project__ = 'NutFlask'
import sqlite3


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
class User:
    def __init__(self,_id,username,password):
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls,username):
        connection = sqlite3.connect(r'C:\Users\me\Source\Repos\NutFlask\models\NutFlaskTestData.db')
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
    def find_by_id(cls,username):
        connection = sqlite3.connect('NutFlaskTestData.db')
        cursor = connection.cursor()

        query = "SELECT * from users WHERE _id=?"
        result = cursor.execute(query,(username,))
        row = result.fetchone()
        if row:
            user = cls(*row)
        else:
            user = None
        connection.close()
        return user
