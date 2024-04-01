from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, SelectField
from wtforms.validators import DataRequired, ValidationError

#Define Student Course Choice
course_choices = [
    ('course1', 'Course 1'),
    ('course2', 'Course 2'),
    ('course3', 'Course 3'),
    ('course4', 'Course 4'),
    ('course5', 'Course 5')
]

class StudentForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    student_id = IntegerField('Student ID', validators=[DataRequired()])
    first_course_choice = SelectField('First Course Choice', choices=course_choices, validators=[DataRequired()])
    second_course_choice = SelectField('Second Course Choice', choices=course_choices, validators=[DataRequired()])
    third_course_choice = SelectField('Third Course Choice', choices=course_choices, validators=[DataRequired()])
    fourth_course_choice = SelectField('Fourth Course Choice', choices=course_choices, validators=[DataRequired()])
    fifth_course_choice = SelectField('Fifth Course Choice', choices=course_choices, validators=[DataRequired()])
    submit = SubmitField('Submit')
