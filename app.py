from flask import Flask
from flask_restful import Api

from common.database import Database
from models.ingredient import Ingredient
from flask_jwt import JWT,jwt_required

from models.product import Product
from security import authenticate, identity
from models.user import UserRegister



app = Flask(__name__)
app.debug = True
app.secret_key = "jose"
api = Api(app)

jwt = JWT(app, authenticate, identity) #/auth


@app.before_first_request
def int_db():
    Database.initialize()
myView = Ingredient.as_view("ingredient_api")
userView = UserRegister.as_view("user_register_api")
productView = Product.as_view("product_api")
app.add_url_rule("/ingredient/create", methods=['POST'], view_func=myView)
app.add_url_rule('/ingredient/list', methods=['GET'], defaults={'name' : None}, view_func=myView)
app.add_url_rule("/ingredient/view/<string:name>",methods=['GET'], view_func=myView)
app.add_url_rule("/ingredient/update/",methods=['PUT'], view_func=myView)
app.add_url_rule("/ingredient/delete/<string:name>",methods=['DELETE'], view_func=myView)
app.add_url_rule("/user/register/",methods=['POST','DELETE','PUT'], view_func=userView)
# product
app.add_url_rule("/product/create",methods=['POST'], view_func=productView)
app.add_url_rule("/product/edit",methods=['PUT'], view_func=productView)
app.add_url_rule("/product/list",methods=['GET'], view_func=productView)
app.add_url_rule("/product/view/<string:name>",methods=['GET'], view_func=productView)
#app.add_url_rule("/auth",methods=None,view_func=myView)
if __name__ == '__main__':
    app.run(port=5000, debug=True)

