from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, SelectField
from wtforms.validators import DataRequired, ValidationError, NumberRange, Optional
from flaskapp.models import SupervisorStudentRanking, Student, Course
from .extensions import db
from flaskapp.init_scenario import get_active_configuration

#Supervisorform 
class SupervisorForm(FlaskForm):
    supervisor = StringField('Supervisor', validators=[DataRequired()])
    course = SelectField('Course', validators=[DataRequired()])
    first_student_choice = SelectField('First Student Choice', validators=[DataRequired()])
    second_student_choice = SelectField('Second Student Choice', validators=[DataRequired()])
    third_student_choice = SelectField('Third Student Choice', validators=[DataRequired()])
    fourth_student_choice = SelectField('Fourth Student Choice', validators=[DataRequired()])
    fifth_student_choice = SelectField('Fifth Student Choice', validators=[DataRequired()])
    capacity = SelectField('Capacity', choices=[(1, '1'), (2, '2'), (3, '3')], validators=[Optional()])
    submit = SubmitField('Submit')

    #fetching choices from SQLite db 
    def __init__(self, *args, **kwargs):
        super(SupervisorForm, self).__init__(*args, **kwargs)
        self.active_config = get_active_configuration()

        #populating course choices to drop down 
        self.course.choices = [(course.id, course.name) for course in Course.query.all()]

        #populating students from db to drop down 
        self.first_student_choice.choices = [(student.student_number, f"{student.student_number} - {student.name}") for student in Student.query.all()]
        self.second_student_choice.choices = [(student.student_number, f"{student.student_number} - {student.name}") for student in Student.query.all()]
        self.third_student_choice.choices = [(student.student_number, f"{student.student_number} - {student.name}") for student in Student.query.all()]
        self.fourth_student_choice.choices = [(student.student_number, f"{student.student_number} - {student.name}") for student in Student.query.all()]
        self.fifth_student_choice.choices = [(student.student_number, f"{student.student_number} - {student.name}") for student in Student.query.all()]

        if self.active_config == 'limited_capacities':
            self.capacity.validators = [DataRequired()]
        else:
            self.capacity.validators = [Optional()]
            self.capacity.data = '1'

    def validate(self, **kwargs):
        
            if not super().validate(**kwargs):
                return False

            # Checking if any of the fields are empty
            if not all(field.data for field in [
                self.supervisor,
                self.course,
                self.first_student_choice,
                self.second_student_choice,
                self.third_student_choice,
                self.fourth_student_choice,
                self.fifth_student_choice
            ]):

                raise ValidationError('Please fill in all the necessary fields.')

            # Checking for duplicate student choices
            chosen_students = [
                self.first_student_choice.data,
                self.second_student_choice.data,
                self.third_student_choice.data,
                self.fourth_student_choice.data,
                self.fifth_student_choice.data
            ]
            if len(chosen_students) != len(set(chosen_students)):
                self.first_student_choice.errors.append("Each student can only be picked once.")
                return False

                # Check for existing supervisors by name
            existing_supervisor = SupervisorStudentRanking.query.filter_by(supervisor=self.supervisor.data).first()
            if existing_supervisor:
                self.supervisor.errors.append("A supervisor with the same name already exists.")
                return False
            
            return True
