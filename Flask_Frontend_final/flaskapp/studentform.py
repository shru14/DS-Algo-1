from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, SelectField
from wtforms.validators import DataRequired, ValidationError, NumberRange
from flaskapp.models import Course, StudentCourseChoice
from .extensions import db


#Dynamic input 
class StudentForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    student_number = IntegerField('Student Number', validators=[DataRequired()])
    first_course_choice = SelectField('First Course Choice', validators=[DataRequired()])
    second_course_choice = SelectField('Second Course Choice', validators=[DataRequired()])
    third_course_choice = SelectField('Third Course Choice', validators=[DataRequired()])
    fourth_course_choice = SelectField('Fourth Course Choice', validators=[DataRequired()])
    fifth_course_choice = SelectField('Fifth Course Choice', validators=[DataRequired()])
    submit = SubmitField('Submit')


    def __init__(self, *args, **kwargs):
        super(StudentForm, self).__init__(*args, **kwargs)
        self.first_course_choice.choices = [(c.id, c.name) for c in Course.query.all()]
        self.second_course_choice.choices = [(c.id, c.name) for c in Course.query.all()]
        self.third_course_choice.choices = [(c.id, c.name) for c in Course.query.all()]
        self.fourth_course_choice.choices = [(c.id, c.name) for c in Course.query.all()]
        self.fifth_course_choice.choices = [(c.id, c.name) for c in Course.query.all()]

#Error handling 
    def validate(self):
        # Call the base class validate
        if not super().validate():
            return False

        # Check if any of the fields are empty
        if not all([self.name.data, self.student_number.data, self.first_course_choice.data,
                    self.second_course_choice.data, self.third_course_choice.data,
                    self.fourth_course_choice.data, self.fifth_course_choice.data]):
            raise ValidationError('Please fill in all the necessary fields.')
            return False

        # Check for duplicate course choices
        course_choices = [self.first_course_choice.data, self.second_course_choice.data,
                          self.third_course_choice.data, self.fourth_course_choice.data,
                          self.fifth_course_choice.data]
        if len(course_choices) != len(set(course_choices)):
            self.first_course_choice.errors.append("Each course can only be picked once.")
            return False

        # Check for existing student by student_number and name
        existing_student = StudentCourseChoice.query.filter_by(student_number=self.student_number.data).first()
        if existing_student:
            if existing_student.name == self.name.data:
                self.student_number.errors.append("A student with the same student number and name already exists.")
                return False
            else:
                # Update the existing record
                existing_student.name = self.name.data
                existing_student.first_course_choice = self.first_course_choice.data
                existing_student.second_course_choice = self.second_course_choice.data
                existing_student.third_course_choice = self.third_course_choice.data
                existing_student.fourth_course_choice = self.fourth_course_choice.data
                existing_student.fifth_course_choice = self.fifth_course_choice.data
                db.session.commit()
                return True
        return True
