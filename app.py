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

api.add_resource(Ingredient_rest, '/ingredient/<string:name>', endpoint = 'ingredient')


@app.before_first_request
def int_db():
    Database.initialize()



if __name__ == '__main__':
    app.run(port=5000, debug=True)

