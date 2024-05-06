from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, SelectField
from wtforms.validators import DataRequired, ValidationError, NumberRange, Optional
from app.models import Course, Student
from app.extensions import db
from app.init_scenario import get_active_configuration

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, Optional, ValidationError
from app.models import Course, Student, StudentCourseChoice
from app.init_scenario import get_active_configuration

class StudentForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    student_number = StringField('Student Number', validators=[DataRequired()])
    course = SelectField('Course', validators=[DataRequired()])
    first_course_choice = SelectField('First Course Choice', choices=[], validators=[DataRequired()])
    second_course_choice = SelectField('Second Course Choice', choices=[], validators=[DataRequired()])
    third_course_choice = SelectField('Third Course Choice', choices=[], validators=[DataRequired()])
    fourth_course_choice = SelectField('Fourth Course Choice', choices=[], validators=[Optional()])
    fifth_course_choice = SelectField('Fifth Course Choice', choices=[], validators=[Optional()])
    course = SelectField('Course', validators=[DataRequired()], default='1')
    submit = SubmitField('Submit')

    def __init__(self, *args, **kwargs):
        super(StudentForm, self).__init__(*args, **kwargs)
        self.active_config = get_active_configuration()

        # Populate course choices dropdown from the Course table
        all_courses = [(course.id, course.name) for course in Course.query.all()]
        self.course.choices = all_courses

        print("Course choices available:", self.course.choices)

        # Adjust validators dynamically based on configuration
        if self.active_config in ['limited_capacities', 'uneven_preferences']:
            # Set choices for the first three fields only and make the rest optional
            limited_choices = all_courses[:3]  # Only the first three courses
            self.first_course_choice.choices = limited_choices
            self.second_course_choice.choices = limited_choices
            self.third_course_choice.choices = limited_choices
            self.fourth_course_choice.choices = [] 
            self.fifth_course_choice.choices = []  
            for field in [self.fourth_course_choice, self.fifth_course_choice]:
                field.validators = [Optional()]
        else:
            # Ensure all fields have choices and are required for other configurations
            self.first_course_choice.choices = all_courses
            self.second_course_choice.choices = all_courses
            self.third_course_choice.choices = all_courses
            self.fourth_course_choice.choices = all_courses
            self.fifth_course_choice.choices = all_courses
            for field in [self.fourth_course_choice, self.fifth_course_choice]:
                field.validators = [DataRequired()]


    def validate(self, **kwargs):
        if not super().validate(**kwargs):
            return False

        required_choices = [self.first_course_choice, self.second_course_choice, self.third_course_choice]
        if self.active_config not in ['limited_capacities', 'uneven_preferences']:
            required_choices.extend([self.fourth_course_choice, self.fifth_course_choice])

        if any(not choice.data for choice in required_choices):
            raise ValidationError('Please fill in all required course choices.')

        chosen_courses = [choice.data for choice in required_choices if choice.data]
        if len(chosen_courses) != len(set(chosen_courses)):
            self.first_course_choice.errors.append("Each course can only be picked once.")
            return False

        # Allowed student numbers
        allowed_student_numbers = ['10001', '10002', '10003', '10004', '10005']
        if self.student_number.data not in allowed_student_numbers:
            self.student_number.errors.append('Invalid student number. Please enter a valid student number')
            return False

        if StudentCourseChoice.query.filter_by(student_number=self.student_number.data).first():
            self.student_number.errors.append('This student number is already registered in StudentCourseChoice.')
            return False

        existing_student = Student.query.filter_by(student_number=self.student_number.data).first()
        if existing_student and existing_student.name != self.name.data:
            self.student_number.errors.append("This student number is already registered under a different name. Please verify your student number.")
            return False

        return True
