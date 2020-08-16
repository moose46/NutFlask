from flask import Flask
from flask_restful import Api

from common.database import Database
from models.ingredient_rest import Ingredient_rest
from flask_jwt import JWT,jwt_required
from security import authenticate, identity
from models.user import UserRegister



app = Flask(__name__)
app.debug = True
app.secret_key = "jose"
api = Api(app)

jwt = JWT(app, authenticate, identity) #/auth
#api.security_key = 'kitty'
#app.config["SECRET_KET"] = 'jose'
# @app.route('/')
# def index():
#  ingredients = Ingredient.find()
#  return render_template('index.html', ingredients=Ingredient.find())

#api.add_resource(Ingredient_rest, '/ingredient/<string:name>', endpoint = 'ingredient')


@app.before_first_request
def int_db():
    Database.initialize()
myView = Ingredient_rest.as_view("ingredient_api")
userView = UserRegister.as_view("user_register_api")
app.add_url_rule("/ingredient/create/<string:name>", methods=['POST'], view_func=myView)
app.add_url_rule('/ingredient/list', methods=['GET'], defaults={'name' : None}, view_func=myView)
app.add_url_rule("/ingredient/view/<string:name>",methods=['GET'], view_func=myView)
app.add_url_rule("/ingredient/update/<string:name>",methods=['PUT'], view_func=myView)
app.add_url_rule("/ingredient/delete/<string:name>",methods=['DELETE'], view_func=myView)
app.add_url_rule("/user/register/",methods=['POST'], view_func=userView)
#app.add_url_rule("/auth",methods=None,view_func=myView)
if __name__ == '__main__':
    app.run(port=5000, debug=True)

