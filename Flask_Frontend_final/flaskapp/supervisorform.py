from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, SelectField
from wtforms.validators import DataRequired, ValidationError, NumberRange
from flaskapp.studentform import course_choices
from flaskapp.models import SupervisorStudentRanking
from .extensions import db

#Define Student Course Choice
#Defined list of allowed student numbers --> should create error in student input form if student nr is outside range
student_number = [
    ('', 'Please enter student ranking'),
    ('9991', '9991'),
    ('9992', '9992'),
    ('9993', '9993'),
    ('9994', '9994'),
    ('9995', '9995')
]

class SupervisorForm(FlaskForm):
    supervisor = StringField('Supervisor Name', validators=[DataRequired(message="Please enter your name.")])
    course = SelectField('Course', choices=course_choices, validators=[DataRequired(message="Please select your class.")])
    first_student_choice = SelectField('First Student Choice', choices=student_number, validators=[DataRequired(message="Please enter your ranking.")])
    second_student_choice = SelectField('Second Student Choice', choices=student_number, validators=[DataRequired(message="Please enter your ranking.")])
    third_student_choice = SelectField('Third Student Choice', choices=student_number, validators=[DataRequired(message="Please enter your ranking.")])
    fourth_student_choice = SelectField('Fourth Student Choice', choices=student_number, validators=[DataRequired(message="Please enter your ranking.")])
    fifth_student_choice = SelectField('Fifth Student Choice', choices=student_number, validators=[DataRequired(message="Please enter your ranking.")])
    submit = SubmitField('Submit')

    def validate(self, **kwargs):
            # Call base class validation
            if not super().validate(**kwargs):
                return False

            # Check if any of the fields are empty
            if not all(field.data for field in [
                self.supervisor,
                self.course,
                self.first_student_choice,
                self.second_student_choice,
                self.third_student_choice,
                self.fourth_student_choice,
                self.fifth_student_choice
            ]):
            # Raise custom validation error
                raise ValidationError('Please fill in all the necessary fields.')

            # Check for duplicate student choices
            chosen_students = [
                self.first_student_choice.data,
                self.second_student_choice.data,
                self.third_student_choice.data,
                self.fourth_student_choice.data,
                self.fifth_student_choice.data
            ]
            if len(chosen_students) != len(set(chosen_students)):
                error_message = "Each student can only be picked once."
                # You can attach this error to one of the student choice fields, or a custom field for form-level errors.
                self.first_student_choice.errors.append(error_message)
                # Returning False here indicates validation failure
                return False

                # Check for existing superviros by name
            existing_supervisor = SupervisorStudentRanking.query.filter_by(supervisor=self.supervisor.data).first()
            if existing_supervisor:
                if existing_supervisor.supervisor == self.supervisor.data:
                    error_message_2 = "A supervisor with the same name already exists."
                    self.supervisor.errors.append(error_message_2)
                    return False

                else:
                  
                    return True
            else:
                # No existing student, so proceed
                return True
