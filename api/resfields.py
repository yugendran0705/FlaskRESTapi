from flask_restful import fields

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

