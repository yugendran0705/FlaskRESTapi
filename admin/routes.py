from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token

"""Blueprint for admin routes and functions for login and adding courses for students to register for the course"""
admin = Blueprint('admin', __name__)  # Blueprint for admin


@admin.route('/login', methods=['POST', 'GET'])
def login():
    """Login for admin to get access token for accessing the admin routes and functions """
    password = request.json.get("password")
    if password == "admin":
        access_token = create_access_token(identity="admin")
        response = jsonify(message='success', access_token=access_token)
        return response, 200
    else:
        return jsonify(message='login failed'), 401
