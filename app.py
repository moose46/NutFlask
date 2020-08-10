from flask import Flask
from flask_restful import Api

from common.database import Database
from models.ingredient_rest import Ingredient_rest

app = Flask(__name__)
api = Api(app)


# @app.route('/')
# def index():
#  ingredients = Ingredient.find()
#  return render_template('index.html', ingredients=Ingredient.find())

#api.add_resource(Ingredient_rest, '/ingredient/<string:name>', endpoint = 'ingredient')


@app.before_first_request
def int_db():
    Database.initialize()
myView = Ingredient_rest.as_view("ingredient_api")
app.add_url_rule("/ingredient", methods=['POST'], view_func=myView)
app.add_url_rule('/ingredient', methods=['GET'], defaults={'name' : None}, view_func=myView)
app.add_url_rule("/ingredient/<string:name>",methods=['GET','PUT','DELETE'], view_func=myView)

if __name__ == '__main__':
    app.run(port=5000, debug=True)

