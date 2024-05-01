from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, SelectField
from wtforms.validators import DataRequired, ValidationError, NumberRange
from flaskapp.models import Student, SupervisorStudentRanking, Course
from .extensions import db


class SupervisorForm(FlaskForm):
    supervisor = StringField('Supervisor Name', validators=[DataRequired()])
    course = SelectField('Course', coerce=int, validators=[DataRequired()])
    first_student_choice = SelectField('First Student Choice', validators=[DataRequired()])
    second_student_choice = SelectField('Second Student Choice', validators=[DataRequired()])
    third_student_choice = SelectField('Third Student Choice', validators=[DataRequired()])
    fourth_student_choice = SelectField('Fourth Student Choice', validators=[DataRequired()])
    fifth_student_choice = SelectField('Fifth Student Choice', validators=[DataRequired()])
    capacity = IntegerField('Capacity', validators=[DataRequired(), NumberRange(min=1, message="Capacity must be at least 1")])
    submit = SubmitField('Submit')

    
    def __init__(self, *args, **kwargs):
        super(SupervisorForm, self).__init__(*args, **kwargs)
        self.course.choices = [(course.id, course.name) for course in Course.query.all()]
        self.first_student_choice.choices = [(s.student_number, s.name) for s in Student.query.all()]
        self.second_student_choice.choices = [(s.student_number, s.name) for s in Student.query.all()]
        self.third_student_choice.choices = [(s.student_number, s.name) for s in Student.query.all()]
        self.fourth_student_choice.choices = [(s.student_number, s.name) for s in Student.query.all()]
        self.fifth_student_choice.choices = [(s.student_number, s.name) for s in Student.query.all()]

#Error handling
    def validate(self):
            if not super().validate():
                return False

            # Check if any of the fields are empty
            if not all([self.supervisor.data, self.course.data,
                        self.first_student_choice.data, self.second_student_choice.data,
                        self.third_student_choice.data, self.fourth_student_choice.data,
                        self.fifth_student_choice.data]):
                raise ValidationError('Please fill in all the necessary fields.')
                return False

            # Check for duplicate student choices
            student_choices = [self.first_student_choice.data, self.second_student_choice.data,
                            self.third_student_choice.data, self.fourth_student_choice.data,
                            self.fifth_student_choice.data]
            if len(student_choices) != len(set(student_choices)):
                self.first_student_choice.errors.append("Each student can only be picked once.")
                return False

            # Check for existing supervisor by name
            existing_supervisor = SupervisorStudentRanking.query.filter_by(supervisor=self.supervisor.data).first()
            if existing_supervisor:
                self.supervisor.errors.append("A supervisor with the same name already exists.")
                return False
            return True
