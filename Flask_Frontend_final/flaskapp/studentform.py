from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, SelectField
from wtforms.validators import DataRequired
from flaskapp.models import Course, StudentCourseChoice
from flask import session


class StudentForm(FlaskForm):

    #predfined fields that do not change dynamically
    name = StringField('Name', validators=[DataRequired()])
    student_number = IntegerField('Student Number', validators=[DataRequired()])
    submit = SubmitField('Submit')

    #Initialization to adjust fields dynamically based on configuration 
    #configuration=None passes configuration value to form, by default set to None
    #current configuration is fetched from session in the route
    def __init__(self, configuration=None, *args, **kwargs):

        #passes initialisation of FlaskForm constructor to Studentform 
        super(StudentForm, self).__init__(*args, **kwargs)

        #queries course names from database
        courses = [(c.id, c.name) for c in Course.query.order_by(Course.name).all()]
        
        #rules for dynamic field changes based on configuration
        if configuration == 'even_preferences':
            field_names = ['first_course_choice', 'second_course_choice', 'third_course_choice', 'fourth_course_choice', 'fifth_course_choice']
        elif configuration in ['limited_capacity', 'uneven_preferences']:
            field_names = ['first_course_choice', 'second_course_choice', 'third_course_choice']

        #dynamic drop down fiels based on configuration
        for field_name in field_names:
            setattr(self, field_name, SelectField(field_name.replace('_', ' ').title(), validators=[DataRequired()], choices=courses))

    #checking that all forms are valid
    def validate(self):
        if not super().validate():
            return False

        #checking that all fields are filled
        filled_fields = [getattr(self, f) for f in self.__dict__.keys() if f.endswith('_course_choice')]
        if not all(field.data for field in filled_fields):
            self.errors['course_choices'] = ['Please fill in all the necessary fields.']
            return False

        #each course choice can only be picked once 
        course_choices = [field.data for field in filled_fields]
        if len(course_choices) != len(set(course_choices)):
            self.errors['course_choices'] = ["Each course can only be picked once."]
            return False

        #checking that student numbers are only used once 
        existing_student = StudentCourseChoice.query.filter_by(student_number=self.student_number.data).first()
        if existing_student and existing_student.name == self.name.data:
            self.student_number.errors.append("A student with the same student number and name already exists.")
            return False

        return True