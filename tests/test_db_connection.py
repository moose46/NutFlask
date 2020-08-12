__author__ = 'Robert W. Curtiss'
__project__ = 'Breathing Air Solutions'

from models.ingredient import Ingredient

"""
====================================================
Author: Robert W. Curtiss
    Project: Breathing Air Solutions
    File: test_db_connection
    Created: Jul, 27, 2020
    
    Description:
    
===================================================
"""

from unittest import TestCase
from common.database import Database


class DatabaseTest(TestCase):
    def test010_connection(self):
        db = Database
        db.initialize(False)

    def test011_insert_ingredient(self):
        i = Ingredient("salt_test")
        Ingredient.save_to_mongo(i)
        self.assertTrue(Ingredient.get_by_name("salt_test") is not None)

    def test015_get_salt(self):
        x = Ingredient.get_by_name('salt_test')
        print(x)
        self.assertTrue(x['name'] == 'salt_test')

    # add salt to the database
    def test016_update_salt(self):
        x = Database.find_one('Ingredient',{'name' : 'salt_test'})
        self.assertTrue(x['name'] == 'salt_test')
        x['name'] = 'salt_test1'
        self.assertTrue(x['name'] == 'salt_test1')
        x1 = Database.update('Ingredient',x['_id'],{'name':'salt_test1'})
        self.assertTrue(x1 is not None)
    def test020_get_all(self):
        for x in Ingredient.find():
            print(x)
    #delete salt and make sure that only on item was deleted
    def test030_delete_ingredient(self):
        r = Ingredient.delete_by_name('salt_test1')
        self.assertTrue(r.name.deleted_count == 1)


