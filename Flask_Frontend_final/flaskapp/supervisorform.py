from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, SelectField
from wtforms.validators import DataRequired
from flaskapp.models import Student, SupervisorStudentRanking, Course
from flask import session


class SupervisorForm(FlaskForm):

    #Predefined fields that don't change dynamically
    supervisor = StringField('Supervisor Name', validators=[DataRequired()])
    course = SelectField('Course', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Submit')

    #Initialization to adjust fields dynamically based on configuration 
    #configuration=None passes configuration value to form, by default set to None
    #current configuration is fetched from session in the route
    def __init__(self, configuration=None, *args, **kwargs):
        super(SupervisorForm, self).__init__(*args, **kwargs)

        #dynamically adding students that supervisors can choose from --> technically dynamic fields wouldn't be necessary here but i would like to hardcode as little as possible
        student_choice_fields = ['first_student_choice', 'second_student_choice', 'third_student_choice', 
                                 'fourth_student_choice', 'fifth_student_choice']
        
        #adding drop down fields dynamically 
        for field_name in student_choice_fields:
            setattr(self, field_name, SelectField(field_name.replace('_', ' ').title(), validators=[DataRequired()]))

        #If configuration is set to limited_capacity, then capacity field is addeded
        if configuration == 'limited_capacity':
            self.capacity = IntegerField('Capacity', validators=[DataRequired()])

        #setting choices for the drop down fields
        self.set_choices()

    def set_choices(self):

        #fetching students from db
        students = [(s.student_number, s.name) for s in Student.query.all()]

        #fetchning courses from db
        courses = [(c.id, c.name) for c in Course.query.all()]
        self.course.choices = courses
        for field_name in self._fields:
            if 'student_choice' in field_name:
                field = getattr(self, field_name)
                field.choices = students

    def validate(self):
        if not super().validate():
            return False

        #Error handling: checking for duplicate student choices
        student_choices = [getattr(self, f).data for f in self._fields if 'student_choice' in f]
        if len(student_choices) != len(set(student_choices)):
            for f in self._fields:
                if 'student_choice' in f:
                    field = getattr(self, f)
                    field.errors.append("Each student can only be picked once.")
            return False

        #Error handling: Checkingfor existing supervisor by name
        existing_supervisor = SupervisorStudentRanking.query.filter_by(supervisor=self.supervisor.data).first()
        if existing_supervisor:
            self.supervisor.errors.append("A supervisor with the same name already exists.")
            return False
        
        return True
