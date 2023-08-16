from flask import abort
from flask_restful import Resource,abort,marshal_with
from flask_jwt_extended import jwt_required
from flaskapi.models import Course, Student
from flaskapi import db, bcrypt
from flaskapi.api.resfields import *
from flaskapi.api.reqpar import *
from flaskapi.api.errors import *
#-------------------------------------------------------------  Resources  -------------------------------------------------------------------------------------
"""Flask restful defines the resource class, which contains methods for each HTTP method that the resource supports."""
"""Resources for Student"""

"""Registering the Student_ resource"""


"""Resources for Admin"""
class Admins(Resource):
    @marshal_with(resource_fields_course)
    @jwt_required()
    def get(self):
        """Get all courses"""
        course_=Course.query.all()
        return course_, 200
    
    @marshal_with(resource_fields_course)
    @jwt_required()
    def post(self):
        """Add course to the database"""
        args = course_post_args.parse_args()
        abort_if_course_exist(args['courses'])
        course_ = Course(courses=args['courses'])
        db.session.add(course_)
        db.session.commit()
        return course_, 201
    
    @marshal_with(resource_fields)
    @jwt_required()
    def patch(self):
        """Update student details"""
        args = student_update_args.parse_args()
        reg_number = args['registration_number']
        result = Student.query.filter_by(registration_number=reg_number).first()
        if not result:
            abort(404, message="Student doesn't exist, cannot update")
        course=Course.query.filter_by(courses=args['course']).first()
        if not course:
            abort(404, message="Course doesn't exist")
        if args['name']:
            result.name = args['name']
        if args['age']:
            result.age = args['age']
        if args['course']:
            result.course = args['course']
        if args['password']:
            hashed_password = bcrypt.generate_password_hash(args['password']).decode('utf-8')
            result.password = hashed_password
        db.session.commit()
        return result, 201
    
    @jwt_required()
    def delete(self):
        """Delete student and course details"""
        args = course_post_args.parse_args()
        if args['courses'] is None and args['register_number'] is None:
            #abort(404, message="Doesn't exist")
            return '', 204
        if args['courses'] :
            abort_if_course_doesnt_exist(args['courses'])
            db.session.delete(Course.query.filter_by(courses=args['courses']).first())
            db.session.commit()
            return '', 204
        if args['register_number']:    
            abort_if_student_doesnt_exist(args['registration_number'])
            db.session.delete(Student.query.filter_by(registration_number=args['registration_number']).first())
            db.session.commit()
            return '', 204
