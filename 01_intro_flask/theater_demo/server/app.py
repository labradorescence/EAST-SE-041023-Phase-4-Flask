#!/usr/bin/env python3

# 1. Navigate to `models.py`

# 2a. Set Up Imports
from flask import Flask, request, jsonify, make_response #import flask
from flask_migrate import Migrate #for migration/for alembic
from models import db, Production #import sql alchemy database and Production class
 
# 2b. Create instance of Flask
app = Flask(__name__)

# 2c. Configure the flask app to connect to a database
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///app.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False #as per canvas

# 2d. Enable Alembic by using `Migrate`
migrate = Migrate(app, db)

# 2e. Connect the db to the app
db.init_app(app)

# 3. Migrate the Production model


# $flask db init - creates migrations, instance, pycache folders
# $flask db migrate - migrate
# $flask db update 
# $flask db revision --autogenerate -m 'Create tables productions' 
# (or flask db migrate)
# $flask db upgrade

#flask configuration
# $export FLASK_APP=app.py
# $export FLASK_RUN_PORT=5555


# 4-5. Navigate to `seed.rb`

# 6. Create a / route that returns Hello World
@app.route('/')
def index():
    return '<h1>Hello World!</h1>'
# 6a. Run `flask run --debug` to check if its in the browser



#7. Create a path to retrieve the longest movie
# 7a. Import jsonify, make_response
# 7b. Use the `route` decorator
@app.route('/longest-movies')
def get_longest_movies():
    # 7c. Query for the longest movie
    movie = Production.query.order_by(Production.length.desc()).first()

    # 7d. Jsonify and return the response
    prod = {
        "title": movie.title,
        "genre": movie.genre,
        "length": movie.length
    }
    return make_response(jsonify(prod), 200)






# 8. Create a dynamic route
# 8a. Use the route decorator
@app.route('/productions/<string:title>') #use the pointy bracket/angle bracket/chevron bracket to get str
# 8b. Create productions() to filter through db
def production(title):
    quer = Production.query.filter_by(title=title).first()
    production = {
        "title": quer.title,
        "genre": quer.genre,
        "length": quer.length
    }
    # 8c. Return result as JSON
    return make_response(jsonify(production))







# 9. View the path and host with request context
# 9a. Import 'request'
# 9b. Create route `context` 
@app.route("/context")
def context():
    # 9c. use ipdb
    # import ipdb; 
    # ipdb.set_trace()
    print(" ===== In context ====== ")
    return f'''
    <h1>
    Path     : {request.path} 
    </h1>

    <h1>
    Host     : {request.host}
    </h1>
    '''






# 10. Use the before_request request hook, what this hook does is up to you. You could hit a breakpoint, print something to server console or anything else you can think of.

@app.before_request
def runs_before():
    cur_user = {"user_id": 3, "username": "spiderman"}
    print("-------- BEFORE REQUEST------ ", cur_user)




# Note: If you'd like to run the application as a script instead of using `flask run`, uncomment the line below 
# and run `python app.py`

if __name__ == '__main__':
    app.run(port=5555, debug=True)