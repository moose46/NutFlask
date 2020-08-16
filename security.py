__author__ = 'Robert W. Curtiss'
__project__ = 'Breathing Air Solutions'

"""
====================================================
Author: Robert W. Curtiss
    Project: Ingredient
    File: security
    Created: Aug, 12, 2020
    
    Description:
    
===================================================
"""
from werkzeug.security import safe_str_cmp
from models.user import User

# users = {
#     User(1,'bob','123'),
#     User(2,'carol','123')
# }
# username_mapping = {u.username: u for u in users}
# userid_mapping = {u.id: u for u in users}

def authenticate(username, password):
    user = User.find_by_username(username)
    if user and safe_str_cmp(user.password,password):
        return user

def identity(payload):
    user_id = payload['identity']
    return User.find_by_id(user_id)
