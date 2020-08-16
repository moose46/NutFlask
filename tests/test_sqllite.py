__author__ = 'Robert W. Curtiss'
__project__ = 'NutFlask'

"""
====================================================
Author: Robert W. Curtiss
    Project: NutFlask
    File: test_sqllite
    Created: Aug, 15, 2020
    
    Description:
    
===================================================
"""
from unittest import TestCase
from models.user import User

class UserTest(TestCase):
    def test010_find_bob_by_name(self):
        user = User.find_by_username('bob')
        self.assertTrue(user.username == 'bob')
