from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, SelectField
from wtforms.validators import DataRequired, ValidationError, NumberRange, Optional
from app.models import SupervisorStudentRanking, Student, Course
from .extensions import db
from app.init_scenario import get_active_configuration

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

    #fetching inputs for form drop downs from db
    def __init__(self, *args, **kwargs):
        super(SupervisorForm, self).__init__(*args, **kwargs)
        self.active_config = get_active_configuration()

        #fetching entire course list from db
        all_courses = [(course.id, course.name) for course in Course.query.all()]

        #Limiting course list if config: limited_capacities or uneven_preferences
        if self.active_config in ['limited_capacities', 'uneven_preferences']:
            limited_courses = all_courses[:3]  # Only the first three courses
            self.course.choices = limited_courses
        else:
            self.course.choices = all_courses

        #populating students to drop down 
        all_students = [(student.student_number, f"{student.student_number} - {student.name}") for student in Student.query.all()]
        for field in [self.first_student_choice, self.second_student_choice, self.third_student_choice, self.fourth_student_choice, self.fifth_student_choice]:
            field.choices = all_students

        #activating capacities field for config:limited capacities
        if self.active_config == 'limited_capacities':
            self.capacity.validators = [DataRequired()]
        else:
            self.capacity.validators = [Optional()]
            self.capacity.data = '1'

    def validate(self, **kwargs):
        
            if not super().validate(**kwargs):
                return False

            # Ensuring that all fields are filled
            if not all([self.supervisor.data, self.course.data, self.first_student_choice.data,
                        self.second_student_choice.data, self.third_student_choice.data,
                        self.fourth_student_choice.data, self.fifth_student_choice.data]):
                raise ValidationError("All fields must be filled out.")

            # Checking for duplicate student selections
            student_choices = [self.first_student_choice.data, self.second_student_choice.data,
                                self.third_student_choice.data, self.fourth_student_choice.data,
                                self.fifth_student_choice.data]
            if len(student_choices) != len(set(student_choices)):
                error_msg = "Each student can only be picked once."
                self.first_student_choice.errors.append(error_msg)

            # Checking for duplicate supervisors by name
            if SupervisorStudentRanking.query.filter_by(supervisor=self.supervisor.data).first():
                self.supervisor.errors.append("A supervisor with this name has already submitted a ranking.")

            # Checking if the selected course is already assigned to a different supervisor
            existing_assignment = SupervisorStudentRanking.query.filter_by(course=self.course.data).first()
            if existing_assignment:
                self.course.errors.append("This course is already assigned to another supervisor. Please select a different course.")
                return False

            
            return True


