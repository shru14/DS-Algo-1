from flask import Flask
from .extensions import db
from .models import Student, Course, Configuration
from .init_scenario import init_configurations


#Creating flaskapp
def create_app(config_filename='config.py'):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile(config_filename)
    app.config.from_pyfile('instance/config.py', silent=True)

    db.init_app(app)

    with app.app_context():
        db.create_all() 

        #Initializing + populating configurations
        if not Configuration.query.first():
            init_configurations()

        #Initializing + populating student + course db
        if not db.session.query(Student).first() or not db.session.query(Course).first():
            populate_database(app) 

        from . import routes

    return app


#function for populating database with predefined entries (course + student list)
def populate_database(app):
    with app.app_context(): 
        with db.session.begin():

            courses = [
                Course(name="1 - The Science of Spaghetti"),
                Course(name="2 - Engineering Toast Hawaii"),
                Course(name="3 - The Evolution of Ketchup"),
                Course(name="4 - Apples and Oranges? A Philosophical Perspective"),
                Course(name="5 - A Cross-Cultural Approach to Sparkling Water")
            ]
            db.session.bulk_save_objects(courses)

            students = [
                Student(student_number=10001, name="Bob"),
                Student(student_number=10002, name="Alice"),
                Student(student_number=10003, name="Tom"), 
                Student(student_number=10004, name="Jim"),
                Student(student_number=10005, name="Lisa")
            ]
            db.session.bulk_save_objects(students)
            db.session.commit()
