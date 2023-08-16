from flask import Flask, jsonify, request, Blueprint
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token,JWTManager, jwt_required

db = SQLAlchemy() # Create a database object
jwt = JWTManager() # Create a JWT object
bcrypt = Bcrypt() # Create a bcrypt object


def create_app():
    app = Flask(__name__)
    api = Api(app) # Create a flask restful api
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db' # Create a database
    app.config['JWT_SECRET_KEY'] = 'secret'  # Change this!
    #app.config.from_object(config_filename)
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    from flaskapi.api.studentres import Students # Importing the student resource
    from flaskapi.api.adminres import Admins # Importing the admin resource
    from flaskapi.student.routes import student # Importing the student blueprint
    from flaskapi.admin.routes import admin # Importing the admin blueprint

    app.register_blueprint(student, url_prefix="/student") # Registering the student blueprint
    app.register_blueprint(admin, url_prefix="/admin") # Registering the admin blueprint
    api.add_resource(Admins, "/admin")   
    api.add_resource(Students, "/student")


    return app
