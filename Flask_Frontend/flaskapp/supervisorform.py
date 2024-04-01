from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, SelectField
from wtforms.validators import DataRequired, ValidationError

#Define Student Course Choice
student_choices = [
    ('student1', 'Student 1'),
    ('student2', 'Student 2'),
    ('student3', 'Student 3'),
    ('student4', 'Student 4'),
    ('student5', 'Student 5')
]

class SupervisorForm(FlaskForm):
    course = StringField('Course Title', validators=[DataRequired()])
    first_student_choice = SelectField('First Student Choice', choices=student_choices, validators=[DataRequired()])
    second_student_choice = SelectField('Second Student Choice', choices=student_choices, validators=[DataRequired()])
    third_student_choice = SelectField('Third Student Choice', choices=student_choices, validators=[DataRequired()])
    fourth_student_choice = SelectField('Fourth Student Choice', choices=student_choices, validators=[DataRequired()])
    fifth_student_choice = SelectField('Fifth Student Choice', choices=student_choices, validators=[DataRequired()])
    submit = SubmitField('Submit')
