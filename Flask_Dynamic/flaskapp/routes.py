from typing import NotRequired
from flask import render_template, flash, redirect, url_for, request
from flask import current_app as app
from wtforms import StringField
from .extensions import db
from flaskapp.models import StudentCourseChoice, SupervisorStudentRanking, Match, Configuration, Course, Student
from flaskapp.studentform import StudentForm
from flaskapp.supervisorform import SupervisorForm
from flaskapp.GS import perform_matching
from flaskapp.models import Configuration
from flaskapp.admin import ConfigForm
from wtforms import SelectField, StringField
from flaskapp.init_scenario import get_active_configuration
from flaskapp.admin import ConfigForm  

# Route for the home page, which is where the blog posts will be shown
@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', title='Course Selection Spring 2024')


# Route for studentform page
@app.route("/studentform", methods=['GET', 'POST'])
def studentform():
    # active config already fetched in studentform, therefore not here
    form = StudentForm()


    if form.validate_on_submit():

     
        selection = StudentCourseChoice(
            name=form.name.data,
            student_number=form.student_number.data,
            first_course_choice=form.first_course_choice.data,
            second_course_choice=form.second_course_choice.data,
            third_course_choice=form.third_course_choice.data, 
            fourth_course_choice=form.fourth_course_choice.data,
            fifth_course_choice=form.fifth_course_choice.data
        )

        db.session.add(selection)
        db.session.commit()
        flash('Thank you! Your course selection has been submitted. Your final course allocation will be published shortly.')
        return redirect(url_for('studentform'))
    
    else:
        print("Form errors:", form.errors)
        for fieldName, errorMessages in form.errors.items():
            for err in errorMessages:
                print(f"Error in {fieldName}: {err}")

    # If form validation fails or it's a GET request, render the form template
    return render_template('studentform.html', title='Students: Course Selection', form=form, active_config=form.active_config)
   


#Route for Supervisor page
@app.route("/supervisorform", methods=['GET', 'POST'])
def supervisorform():
    form = SupervisorForm()

    active_config = get_active_configuration()

    if form.validate_on_submit():
        capacity_value = form.capacity.data if active_config == 'limited_capacities' else None
        selection = SupervisorStudentRanking(
            supervisor=form.supervisor.data,
            course=form.course.data,
            first_student_choice=form.first_student_choice.data,
            second_student_choice=form.second_student_choice.data,
            third_student_choice=form.third_student_choice.data,
            fourth_student_choice=form.fourth_student_choice.data,
            fifth_student_choice=form.fifth_student_choice.data,
            capacity=capacity_value
        )

        # For limited capacities, store the selected capacity
        if form.active_config == 'limited_capacities':
            selection.capacity = form.capacity.data

        db.session.add(selection)
        db.session.commit()
        flash('Thank you! Your course selection has been submitted. Your final student allocation will be published shortly.')
        return redirect(url_for('supervisorform'))
    
      # If form validation fails, render the form template with error messages
    # Pass the form object to the template to display error messages next to the fields
    else:
        return render_template('supervisorform.html', title='Supervisors: Student Ranking', form=form, active_config=form.active_config)




#run Matching and return output as table
@app.route('/match', methods=['GET', 'POST'])
def match():
    # Fetching current configuration
    active_config = get_active_configuration()

    if request.method == 'POST':
        # Clear out old matches
        Match.query.delete()
        db.session.commit()

        # Perform matching process
        matches, error = perform_matching()  # Expecting two return values

        if error:
            flash(f'Error during matching: {error}', 'error')
            return redirect(url_for('match'))

        # Create new match objects for each pairing
        if isinstance(matches, dict):
            for student_number, supervisor_ranking_id in matches.items():
                new_match = Match(student_number=student_number, supervisor_ranking_id=supervisor_ranking_id)
                db.session.add(new_match)
            db.session.commit()
            flash('Matching process completed successfully.')
        else:
            flash('Matching failed due to unexpected return type.', 'error')

        # Reload page to view match list
        return redirect(url_for('match'))

    # Fetching all matches and joining with other tables for more detailed output
    all_matches = db.session.query(
        Match.id,
        StudentCourseChoice.student_number,
        StudentCourseChoice.name.label('student_name'),
        SupervisorStudentRanking.course.label('course_number'),
        SupervisorStudentRanking.supervisor.label('supervisor_name')
    ).join(
        StudentCourseChoice, StudentCourseChoice.student_number == Match.student_number
    ).join(
        SupervisorStudentRanking, SupervisorStudentRanking.id == Match.supervisor_ranking_id
    ).all()

    # Print debugging information
    print("Active Configuration:", active_config)
    print("Number of Matches:", len(all_matches))

    # Create a detailed list of match information for the template
    detailed_matches = [{
        'match_id': match_id,
        'student_name': student_name,
        'student_number': student_number,
        'course_number': course_number,
        'supervisor_name': supervisor_name
    } for match_id, student_number, student_name, course_number, supervisor_name in all_matches]

    return render_template('match.html', matches=detailed_matches, active_config=active_config, num_matches=len(all_matches))


#Admin Route 
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    form = ConfigForm()
    if request.method == 'POST' and form.validate_on_submit():

        # Retrieving active configuration
        config = Configuration.query.filter_by(key='active_configuration').first()
        if not config:
            config = Configuration(key='active_configuration')
            db.session.add(config)

        # Clearing relevant tables before updating the configuration
        if config.value != form.configuration.data:  # Check if configuration actually changes
            db.session.query(StudentCourseChoice).delete()
            db.session.query(SupervisorStudentRanking).delete()
            db.session.query(Match).delete()

            db.session.commit()  
        
        # Updating configuration
        config.value = form.configuration.data
        db.session.commit()

        flash('Configuration updated successfully.')
        return redirect(url_for('admin'))

    return render_template('admin.html', form=form)