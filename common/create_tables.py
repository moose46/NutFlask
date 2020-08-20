__author__ = 'Robert W. Curtiss'
__project__ = 'NutFlask'

"""
====================================================
Author: Robert W. Curtiss
    Project: NutFlask
    File: create_tables
    Created: Aug, 16, 2020
    
    Description:
    
===================================================
"""
import sqlite3
from common.globals import SQLITE_DB



connection = sqlite3.connect(SQLITE_DB)
cursor = connection.cursor()
create_table = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)"
cursor.execute(create_table)

create_table = "CREATE TABLE IF NOT EXISTS ingredient (id INTEGER PRIMARY KEY, name text, usage text, side_effects text)"
cursor.execute(create_table)

connection.commit()
connection.close()
