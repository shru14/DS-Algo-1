from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField
from wtforms.validators import DataRequired

configurations = [
    ('', 'Select a configuration'),
    ('default', 'Default'), 
    ('limited_capacities', 'Limited Capacities'), 
    ('uneven_preferences', 'Uneven Preferences')
]

class ConfigForm(FlaskForm):
    configuration = SelectField('Configuration', choices=configurations, validators=[DataRequired(message="Please enter configuration setting.")])
    submit = SubmitField('Save Changes')
