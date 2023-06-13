#5a. Import SerializerMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin

db = SQLAlchemy()

'''
production: the menu
    roles: margot 
        ---
        production: the menu
            roles: margot
                production: the menu
'''

#5b. Add SerializerMixin to the Production Model -> app.py
class Production(db.Model, SerializerMixin):
    __tablename__ = "productions"

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    title = db.Column(db.String) 
    genre = db.Column(db.String)
    length = db.Column(db.Integer) 
    year = db.Column(db.Integer) 
    image = db.Column(db.String)
    language = db.Column(db.String)
    director = db.Column(db.String)
    description = db.Column(db.String) 
    composer = db.Column(db.String)

    # 6. Add serializer rule to remove updated_at and created_at
    serialize_rules = ('-created_at', '-updated_at', '-roles.production')
    # 8a. Add serializer rules to avoid max recursion


    # 7b. Create the relationship between Role and Production
    roles = db.relationship('Role', back_populates='production')

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# 7a. Create a class Role with ForeignKey to production, and string:role_name : 
class Role(db.Model, SerializerMixin):
    __tablename__ = "roles" 

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    role_name = db.Column(db.String)
    production_id = db.Column(db.Integer, db.ForeignKey('productions.id'))

    #7b. Create the relationship between Role and Production -> seed.py
    production = db.relationship('Production', back_populates='roles')
    # 8b. Add serializer rules to avoid max recursion -> [You Do] app.py to write routes for Roles
    serialize_rules = ('-created_at', '-updated_at', '-production.roles')


    
