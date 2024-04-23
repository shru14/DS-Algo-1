from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, SelectField
from wtforms.validators import DataRequired, ValidationError, NumberRange

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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Update choices for subsequent course choices based on previous selections
        self.second_course_choice.choices = self._get_filtered_course_choices([])
        self.third_course_choice.choices = self._get_filtered_course_choices([self.first_course_choice.data])
        self.fourth_course_choice.choices = self._get_filtered_course_choices(
            [self.first_course_choice.data, self.second_course_choice.data])
        self.fifth_course_choice.choices = self._get_filtered_course_choices(
            [self.first_course_choice.data, self.second_course_choice.data, self.third_course_choice.data])

    def _get_filtered_course_choices(self, selected_courses):
        # Filter out selected courses from the available course choices
        filtered_choices = [(value, label) for value, label in course_choices if value not in selected_courses]
        return filtered_choices

    def validate(self):
        # Call base class validation
        if not super().validate():
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

        # Check for duplicate course selections
        selected_courses = [
            self.first_course_choice.data,
            self.second_course_choice.data,
            self.third_course_choice.data,
            self.fourth_course_choice.data,
            self.fifth_course_choice.data
        ]
        if len(selected_courses) != len(set(selected_courses)):
            # Get the indices of duplicate course selections
            duplicates = set([course for course in selected_courses if selected_courses.count(course) > 1])
            for field in [self.first_course_choice, self.second_course_choice, self.third_course_choice,
                          self.fourth_course_choice, self.fifth_course_choice]:
                if field.data in duplicates:
                    field.errors.append('Please select each course only once.')  # Append error message to the field

            # Raise validation error
            raise ValidationError('Please select each course only once.')

        return True
