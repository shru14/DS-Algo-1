from flask import Flask
from .extensions import db
from .models import Student, Course, Configuration


def create_app(config_filename='config.py'):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile(config_filename)
    app.config.from_pyfile('instance/config.py', silent=True)

    db.init_app(app)

    # Importing routes and models within the context
    with app.app_context():
        db.create_all() 

        # Populate the database if it's empty
        if not db.session.query(Student).first() or not db.session.query(Course).first():
            populate_database(app)  
        #initializing configurations
        init_configurations(app) 

        from . import routes, models
        
    return app



def populate_database(app):
    with app.app_context():  
        #Populating db with course list
        courses = [
            Course(name="1 - The Science of Spaghetti"),
            Course(name="2 - Engineering Toast Hawaii"),
            Course(name="3 - The Evolution of Ketchup"),
            Course(name="4 - Apples and Oranges? A Philosophical Perspective"),
            Course(name="5 - A Cross-Cultural Approach to Sparkling Water")
        ]
        db.session.bulk_save_objects(courses)

        #Populating db with student list
        students = [
            Student(student_number=10001, name="Bob"),
            Student(student_number=10002, name="Alice"),
            Student(student_number=10003, name="Tom"), 
            Student(student_number=10004, name="Jim"),
            Student(student_number=10005, name="Lisa")
        ]
        db.session.bulk_save_objects(students)
        db.session.commit()


def init_configurations(app):
    with app.app_context():
        with db.session.begin_nested():
            # Clear existing data (optional)
            db.session.query(Configuration).delete()

            # Insert new configuration values
            configurations = [
                Configuration(key='even_preferences', value='1'),
                Configuration(key='limited_capacity', value='2'),
                Configuration(key='uneven_preferences', value='3')
            ]
            db.session.add_all(configurations)

        db.session.commit()
