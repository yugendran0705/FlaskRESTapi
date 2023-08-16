from flask_restful import Resource,abort,marshal_with
from flaskapi.models import Student, Course
from flaskapi import db, bcrypt
from flaskapi.api.resfields import *
from flaskapi.api.reqpar import *
from flask_jwt_extended import jwt_required


class Students(Resource):
    @marshal_with(resource_fields)
    @jwt_required()
    def get(self):
        """Get student details by registration number"""
        reg_number = student_get_args.parse_args()['registration_number']
        result = Student.query.filter_by(registration_number=reg_number).first()
        if not result:
            abort(404, message="Could not find student with that registration number")
        return result, 200
    
    @marshal_with(resource_fields)
    def post(self):
        """Add student details to the database"""
        args = student_post_args.parse_args()
        reg_number = args['registration_number']
        result = Student.query.filter_by(registration_number=reg_number).first()
        if result:
            abort(409, message="Student registration number taken...")
        course_check = Course.query.filter_by(courses=args['course']).first()
        if not course_check:
            abort(404, message="Course doesn't exist")
        hashed_password = bcrypt.generate_password_hash(args['password']).decode('utf-8')
        student = Student(registration_number=reg_number, name=args['name'], age=args['age'], course=args['course'], password=hashed_password)
        db.session.add(student)
        db.session.commit()
        return student, 201
