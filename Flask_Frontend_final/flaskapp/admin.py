from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField
from wtforms.validators import DataRequired
from .models import Configuration

configurations = [
    ('', 'Select a configuration'),
    ('even_preferences', 'Even Preferences'), 
    ('limited_capacity', 'Limited Capacities'), 
    ('uneven_preferences', 'Uneven Preferences')
]

#class for configuration selection in admin panel 
class ConfigForm(FlaskForm):
    configuration = SelectField('Configuration', choices=configurations, validators=[DataRequired(message="Please enter configuration setting.")])
    submit = SubmitField('Save Changes')





