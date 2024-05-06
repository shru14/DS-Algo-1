from flask import Flask, render_template, redirect, url_for, request
from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length
import secrets

# This is a working, local version. It takes a Flask Form and lets us input "Name" and "Preferences".
# Input is saved to /data tab of this app. Working on a solution to save the data to a pyhtion list, so we can use it later.

app = Flask(__name__)
# key = secrets.token_urlsafe(16)
# app.secret_key = key

 
@app.route('/form')
def form():
    return render_template('form.html')
 
@app.route('/data/', methods = ['POST', 'GET'])
def data():
    if request.method == 'GET':
        return f"The URL /data is accessed directly. Try going to '/form' to submit form"
    if request.method == 'POST':
        form_data = request.form
        return render_template('data.html',form_data = form_data)
    
# if __name__ == '__main__':
#    app.run(debug=True)
    
