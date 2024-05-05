from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, SelectField
from wtforms.validators import DataRequired, ValidationError, NumberRange
from flaskapp.models import StudentCourseChoice
from flaskapp import db

# Define Student Course Choice
course_choices = [
    ('', 'Select a course'),
    ('course1', 'Course 1'),
    ('course2', 'Course 2'),
    ('course3', 'Course 3'),
    ('course4', 'Course 4'),
    ('course5', 'Course 5')
]

class StudentForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    student_number = IntegerField('Student Number', validators=[DataRequired(message="Please enter your student ID using only numbers."), NumberRange(min=0, message="Your student number should contain only numbers.")])
    first_course_choice = SelectField('First Course Choice', choices=course_choices, validators=[DataRequired()])
    second_course_choice = SelectField('Second Course Choice', choices=course_choices, validators=[DataRequired()])
    third_course_choice = SelectField('Third Course Choice', choices=course_choices, validators=[DataRequired()])
    fourth_course_choice = SelectField('Fourth Course Choice', choices=course_choices, validators=[DataRequired()])
    fifth_course_choice = SelectField('Fifth Course Choice', choices=course_choices, validators=[DataRequired()])
    submit = SubmitField('Submit')

    def validate(self, **kwargs):
        # Call base class validation
        if not super().validate(**kwargs):
            return False

        # Check if any of the fields are empty
        if not all(field.data for field in [
            self.name,
            self.student_number,
            self.first_course_choice,
            self.second_course_choice,
            self.third_course_choice,
            self.fourth_course_choice,
            self.fifth_course_choice
        ]):
        # Raise custom validation error
            raise ValidationError('Please fill in all the necessary fields.')

        # Check for duplicate course choices
        chosen_courses = [
            self.first_course_choice.data,
            self.second_course_choice.data,
            self.third_course_choice.data,
            self.fourth_course_choice.data,
            self.fifth_course_choice.data
        ]
        if len(chosen_courses) != len(set(chosen_courses)):
            error_message = "Each course can only be picked once."
            # You can attach this error to one of the course choice fields, or a custom field for form-level errors.
            self.first_course_choice.errors.append(error_message)
            # Returning False here indicates validation failure
            return False

            # Check for existing student by student_number and name
        existing_student = StudentCourseChoice.query.filter_by(student_number=self.student_number.data).first()
        if existing_student:
            if existing_student.name == self.name.data:
                error_message_2 = "A student with the same student number already exists."
                self.student_number.errors.append(error_message_2)
                return False

            else:
                # If a student with the same student_number but different name exists, replace it
                existing_student.name = self.name.data
                existing_student.first_course_choice = self.first_course_choice.data
                existing_student.second_course_choice = self.second_course_choice.data
                existing_student.third_course_choice = self.third_course_choice.data
                existing_student.fourth_course_choice = self.fourth_course_choice.data
                existing_student.fifth_course_choice = self.fifth_course_choice.data
                db.session.commit()
                return True
        else:
            # No existing student, so proceed
            return True
