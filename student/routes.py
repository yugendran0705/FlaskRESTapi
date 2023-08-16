from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from flaskapi.models import Student, Course
from flaskapi import bcrypt

"""Blueprint for student routes and functions for login and listing courses for students to register for the course"""
"""A blueprint in Flask is an object to structure a Flask application into subsets."""
student = Blueprint(
    'student', __name__)  # Blueprint for student routes and functions


@student.route('/login', methods=['POST', 'GET'])
def login():
    """Login for student to get access token for accessing the student routes and functions """
    reg_num = request.json.get("registration_number")
    password = request.json.get("password")

    student = Student.query.filter_by(registration_number=reg_num).first()

    if student and bcrypt.check_password_hash(student.password, password):
        access_token = create_access_token(identity=reg_num)
        response = jsonify(message='success', access_token=access_token)
        return response, 200
    else:
        return jsonify(message='login failed'), 401


@student.route('/list', methods=['POST', 'GET'])
def list():
    """List of courses for students to register for the course"""
    courses = Course.query.all()
    course_list = {}
    for i in range(len(courses)):
        course_list[i+1] = courses[i].courses
    return jsonify(course_list)
