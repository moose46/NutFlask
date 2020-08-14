__author__ = 'Robert W. Curtiss'
__project__ = 'NutFlask'

"""
====================================================
Author: Robert W. Curtiss
    Project: NutFlask
    File: sqlLiteTest
    Created: Aug, 14, 2020
    
    Description:
    https://www.udemy.com/course/rest-api-flask-and-python/learn/lecture/5965476#overview
===================================================
"""
import sqlite3

connection = sqlite3.connect('NutFlaskTestData.db')

cursor = connection.cursor()

create_table = "CREATE TABLE users (id int, username text, password text)"

cursor.execute(create_table)

user = (1, 'bob','123')
insert_query = "INSERT INTO users VALUES (?,?,?)"
cursor.execute(insert_query,user)

users = [
    (2, 'carol','123'),
    (3, 'stinky','123')
]
cursor.executemany(insert_query,users)

select_query = "SELECT * from users"

for row in cursor.execute(select_query):
    print(row)


connection.commit()
connection.close()


