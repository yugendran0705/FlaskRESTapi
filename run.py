# Description: This file is used to run the application
#------------------------------------------ Imports ------------------------------------------------------------------------------------
from flask import Flask, jsonify, request, Blueprint
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token,JWTManager, jwt_required

app = Flask(__name__) # Create a flask app
api = Api(app) # Create a flask restful api
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db' # Create a database
db = SQLAlchemy(app) # Create a database object
bcrypt = Bcrypt(app) # Create a bcrypt object
app.config['JWT_SECRET_KEY'] = 'secret'  # Change this!
jwt = JWTManager(app) # Create a JWT object

#------------------------------------------------ Database Models -----------------------------------------------------------------------
"""Database Models for Student and Course tables """

class Student(db.Model):
    """Student table model with registration_number, name, age, course and password as columns """
    registration_number = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    course= db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"Student(name = {self.name}, age = {self.age}, course = {self.course}, password = {self.password})"
    
class Course(db.Model):
    """Course table model with courses as columns """
    courses = db.Column(db.String(100), primary_key=True)

    def __repr__(self):
        return f"Course(courses = {self.courses})"

#-------------------------------------------------------------------- Request Parsers --------------------------------------------------    
"""Request parsers are used to parse the arguments passed in the request body"""
"""Request parsers for Student and Course"""

student_post_args = reqparse.RequestParser()
student_post_args.add_argument("registration_number", type=int, help="Registration number of the student is required", required=True)
student_post_args.add_argument("name", type=str, help="Name of the student is required", required=True)
student_post_args.add_argument("age", type=int, help="Age of the student", required=True)
student_post_args.add_argument("course", type=str, help="Course of the student", required=True)
student_post_args.add_argument("password", type=str, help="Password of the student", required=True)

student_update_args = reqparse.RequestParser()
student_update_args.add_argument("registration_number", type=int, help="Registration number of the student is required", required=True)
student_update_args.add_argument("name", type=str, help="Name of the student is required")
student_update_args.add_argument("age", type=int, help="Age of the student")
student_update_args.add_argument("course", type=str, help="Course of the student")
student_update_args.add_argument("password", type=str, help="Password of the student")

student_get_args = reqparse.RequestParser()
student_get_args.add_argument("registration_number", type=int, help="Registration number of the student is required", required=True)

# Request parsers for course
course_post_args = reqparse.RequestParser()
course_post_args.add_argument("courses", type=str, help="Course of the student is required")
course_post_args.add_argument("register_number",type=int)

#------------------------------------------------------------  Error Handling  -------------------------------------------------------------------------------
"""Error handling for student"""

def abort_if_student_doesnt_exist(reg_number):
    if Student.query.filter_by(registration_number=reg_number).first() is None:
        abort(404, message="Student doesn't exist")

# Error handling for course
def abort_if_course_exist(course):
    if Course.query.filter_by(courses=course).first():
        abort(409, message="Course already exist")

def abort_if_course_doesnt_exist(course):
    if Course.query.filter_by(courses=course).first() is None:
        abort(404, message="Course doesn't exist")

#-------------------------------------------------------------  Resource Fields  -------------------------------------------------------------------------------
"""Resource fields are used to define the structure of the data that is returned by the API."""
resource_fields = {
    'registration_number': fields.Integer,
    'name': fields.String,
    'age': fields.Integer,
    'course': fields.String,
    'password': fields.String
}

resource_fields_course = {
    'courses': fields.String
}

#-------------------------------------------------------------  Resources  -------------------------------------------------------------------------------------
"""Flask restful defines the resource class, which contains methods for each HTTP method that the resource supports."""
"""Resources for Student"""
class Student_(Resource):
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

"""Registering the Student_ resource"""
api.add_resource(Student_, "/student")


"""Resources for Admin"""
class Admin(Resource):
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
        abort_if_course_doesnt_exist(args['courses'])
        db.session.delete(Course.query.filter_by(courses=args['courses']).first())
        abort_if_student_doesnt_exist(args['registration_number'])
        db.session.delete(Student.query.filter_by(registration_number=args['registration_number']).first())
        db.session.commit()
        return '', 204
    
"""Registering the resource"""
api.add_resource(Admin, "/admin")   

#---------------------------------------------------------------  Routes  -------------------------------------------------------------------------------
"""Blueprint for student routes and functions for login and listing courses for students to register for the course"""
"""A blueprint in Flask is an object to structure a Flask application into subsets."""
student=Blueprint('student', __name__)  # Blueprint for student

@student.route('/login', methods=['POST','GET'])
def login():
    """Login for student to get access token for accessing the student routes and functions """
    reg_num = request.json.get("registration_number")
    password = request.json.get("password")

    student=Student.query.filter_by(registration_number=reg_num).first()

    if student is not None and bcrypt.check_password_hash(student.password, password):
        access_token = create_access_token(identity=reg_num)
        response =jsonify(message='success', access_token=access_token)
        return response, 200
    else:
        return jsonify(message='login failed'), 401

@student.route('/list', methods=['POST','GET'])
def list():
    """List of courses for students to register for the course"""
    courses = Course.query.all()
    course_list={}
    for i in range(len(courses)):
        course_list[i+1]=courses[i].courses
    return jsonify(course_list)

#-------------------------------------------------------------------------------------------------------------------------------------------------
"""Blueprint for admin routes and functions for login and adding courses for students to register for the course"""
admin=Blueprint('admin', __name__) # Blueprint for admin    

@admin.route('/login', methods=['POST','GET'])
def login():
    """Login for admin to get access token for accessing the admin routes and functions """
    password = request.json.get("password")
    if password == "admin":
        access_token = create_access_token(identity="admin")
        response =jsonify(message='success', access_token=access_token)
        return response, 200
    else:
        return jsonify(message='login failed'), 401


app.register_blueprint(student, url_prefix="/student") # Registering the student blueprint
app.register_blueprint(admin, url_prefix="/admin") # Registering the admin blueprint

#---------------------------------------------------------------  Main  -------------------------------------------------------------------------------

if __name__ == "__main__":
    app.run()
