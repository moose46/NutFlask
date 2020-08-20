__author__ = 'Robert W. Curtiss'
__project__ = 'NutFlask'

"""
====================================================
Author: Robert W. Curtiss
Class: CSCI-1511
    Project: NutFlask
    File: test_users
    Created: Aug, 20, 2020
    
    Description:
    
===================================================
"""
from unittest import TestCase
from common.database import Database
from models.user import User,UserRegister



class DatabaseTest(TestCase):
    def test010_connection(self):
        db = Database
        db.initialize(False)

    def test011_insert_user(self):
        user = User('stinky', '123')
        user.save_to_mongo()
        self.assertTrue(User.get_by_name("stinky") is not None)
