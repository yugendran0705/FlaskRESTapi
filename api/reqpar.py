from flask_restful import reqparse

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

