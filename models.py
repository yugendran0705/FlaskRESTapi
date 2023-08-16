from flaskapi import db


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

