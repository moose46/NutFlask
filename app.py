from flask import Flask, render_template
from flask_restful import Resource, Api

from common.database import Database
from ingredient_rest import Ingredient_rest
from flask.views import MethodView
from models.ingredient import Ingredient

app = Flask(__name__)
api = Api(app)


# @app.route('/')
# def index():
#  ingredients = Ingredient.find()
#  return render_template('index.html', ingredients=Ingredient.find())

api.add_resource(Ingredient_rest, '/ingredient/<string:name>', endpoint = 'ingredient')


@app.before_first_request
def int_db():
    Database.initialize()



if __name__ == '__main__':
    app.run(port=5000, debug=True)

