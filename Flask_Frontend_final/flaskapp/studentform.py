from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, SelectField
from wtforms.validators import DataRequired, ValidationError, NumberRange
from flaskapp.models import StudentCourseChoice
from .extensions import db

#Define Student Course Choice: Starting with course ID for numerical matching
#User sees both name and ID but form submits ID to SQLite Database
course_choices = [
    ('', 'Select a course'),
    ('1', '1 - The Science of Spaghetti'),
    ('2', '2 - Engineering Toast Hawaii'),
    ('3', '3 - The Evolution of Ketchup'),
    ('4', '4 - Apples and Oranges? A Philosophical Perspective'),
    ('5', '5 - A Cross-Cultural Approach to Sparkling Water')
]

class StudentForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(message="Please enter your full name.")])
    student_number = IntegerField('Student Number', validators=[DataRequired(message="Please enter your student ID using only numbers."), NumberRange(min=0, message="Your student number should contain only numbers.")])
    first_course_choice = SelectField('First Course Choice', choices=course_choices, validators=[DataRequired(message="Please enter your first choice.")])
    second_course_choice = SelectField('Second Course Choice', choices=course_choices, validators=[DataRequired(message="Please enter your second choice.")])
    third_course_choice = SelectField('Third Course Choice', choices=course_choices, validators=[DataRequired(message="Please enter your third choice.")])
    fourth_course_choice = SelectField('Fourth Course Choice', choices=course_choices, validators=[DataRequired(message="Please enter your fourth choice.")])
    fifth_course_choice = SelectField('Fifth Course Choice', choices=course_choices, validators=[DataRequired(message="Please enter your fifth choice.")])
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