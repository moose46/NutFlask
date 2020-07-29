from flask import Flask, render_template

from common.database import Database
from models.ingredient import Ingredient

app = Flask(__name__)


@app.route('/')
def index():
    ingredients = Ingredient.find()
    return render_template('index.html', ingredients=Ingredient.find())

@app.before_first_request
def int_db():
    Database.initialize()



if __name__ == '__main__':
    app.run()
