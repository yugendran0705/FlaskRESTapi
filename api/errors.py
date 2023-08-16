from flask_restful import abort
from flaskapi.models import Student, Course

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
