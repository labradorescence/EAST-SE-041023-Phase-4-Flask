#!/usr/bin/env python3

from flask import Flask, jsonify, make_response, request
from flask_migrate import Migrate 
from models import db, Production
import ipdb;

app = Flask(__name__) 
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///app.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False 

migrate = Migrate(app, db) #alembic how we migrate our table for database

db.init_app(app) #db is sqlalchemy database

# | HTTP Verb 	|       Path       	| Description        	|
# |-----------	|:----------------:	|--------------------	|
# | GET       	|   /productions   	| READ all resources 	|
# | GET       	| /productions/:id 	| READ one resource   	|
# | POST      	|   /productions   	| CREATE one resource 	|
# | PATCH/PUT 	| /productions/:id 	| UPDATE one resource	|
# | DELETE    	| /productions/:id 	| DESTROY one resource 	|

@app.route('/')
def index():
    return '<h1>Hello World!</h1>'

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 1. Create a route to /productions for GET requests
@app.route('/productions', methods=["GET", "POST"])
def Productions(): #this function name should be different from model class name that we are importing
    if(request.method == "GET"):

        # 1a. Create the query
        quer = Production.query.all()

        # 1b. Loop through the query and convert each object into a dictionary 
        prods = []
        for each_p in quer:
            prods.append({
                "id": each_p.id,
                "title": each_p.title,
                "genre": each_p.genre,
                "length": each_p.length
            })

        # 1c. Use make_response and jsonify to return a response
        resp = make_response(jsonify(prods), 200)
        return resp
        # 1d. Test in Postman

        # 5c. use SerializerMixin's .to_dict() for responses here and everywhere

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # 3. Create a route to /productions for a POST request
    if(request.method == "POST"):
       # ipdb.set_trace()

        # 3a. Get information from request.get_json() 
        data = request.get_json()

        # 3b. Create new object
        prod = Production(
            title=data.get('title'),
            genre=data.get('genre'),
            length=data.get('length')
        )

        # 3c. Add and commit to db 
        db.session.add(prod)
        db.session.commit()

        # 3d. Convert to dictionary / # 5c. use .to_dict
        prod_dict = {
            "id": prod.id,
            "title": prod.title,
            "genre": prod.genre,
            "length": prod.length
        }

        # prod_dict = prod.to_dict()

        # 3e. return as JSON
        return make_response(jsonify(prod_dict), 201)

        # 3f. Test in postman

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 2. Create a route to /productions/:id for single GET requests
@app.route('/productions/<int:id>', methods=["GET", "DELETE", "PATCH"])
def One_Production(id):
    if(request.method == "GET"):
        #ipdb.set_trace() #debugger trace here
        quer = Production.query.filter_by(id=id).first()
        prod = {
            "id": quer.id,
            "title": quer.title,
            "genre": quer.genre,
            "length": quer.length
        }
        return make_response(jsonify(prod), 200)

        # 5c. use to_dict

    # 4. Create a delete request 
    if(request.method == "DELETE"):
        quer = Production.query.filter_by(id=id).first()
        db.session.delete(quer)
        db.session.commit()
        
        return make_response("deleted :D", 200)


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 5. Serializers: navigate back to models.py 

if __name__ == '__main__':
    app.run(port=5555, debug=True)