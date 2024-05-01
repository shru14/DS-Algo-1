from typing import NotRequired
from flask import render_template, flash, redirect, url_for, request
from flask import current_app as app
from .extensions import db
from flaskapp.models import StudentCourseChoice, SupervisorStudentRanking, Match, Configuration, Course
from flaskapp.studentform import StudentForm
from flaskapp.supervisorform import SupervisorForm
from flaskapp.GS import perform_matching
from flaskapp.models import Configuration
from flaskapp.admin import ConfigForm



# Route for the home page, which is where the blog posts will be shown
@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', title='Course Selection Spring 2024')

'''
# Route for studentform page
@app.route("/studentform", methods=['GET', 'POST'])
def studentform():
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
        return redirect(url_for('home'))
    
     # If form validation fails, render the form template with error messages
    # Pass the form object to the template to display error messages next to the fields
    else:
        return render_template('studentform.html', title='Students: Course Selection', form=form)
'''

#student choice for dynamic input fields 
@app.route('/studentform', methods=['GET', 'POST'])
def studentform():
    form = StudentForm()
    if request.method == 'POST' and form.validate_on_submit():

        # Process the form data, save to database, etc.
        flash('Thank you! Your course selection has been submitted. Your final course allocation will be published shortly.')
        return redirect(url_for('home'))
    
    # If form validation fails, render the form template with error messages
    # Pass the form object to the template to display error messages next to the fields
    else:
        return render_template('studentform.html', title='Students: Course Selection', form=form)
   

'''
#Route for Supervisor page
@app.route("/supervisorform", methods=['GET', 'POST'])
def supervisorform():
    form = SupervisorForm()
    if form.validate_on_submit():
        selection = SupervisorStudentRanking(
            supervisor=form.supervisor.data,
            course=form.course.data,
            first_student_choice=form.first_student_choice.data,
            second_student_choice=form.second_student_choice.data,
            third_student_choice=form.third_student_choice.data, 
            fourth_student_choice=form.fourth_student_choice.data,
            fifth_student_choice=form.fifth_student_choice.data
        )
        db.session.add(selection)
        db.session.commit()
        flash('Thank you! Your course selection has been submitted. Your final student allocation will be published shortly.')
        return redirect(url_for('home'))
    
      # If form validation fails, render the form template with error messages
    # Pass the form object to the template to display error messages next to the fields
    else:
        return render_template('supervisorform.html', title='Supervisors: Student Ranking', form=form)
'''


@app.route('/supervisorform', methods=['GET', 'POST'])
def supervisorform():
    form = SupervisorForm()
    if form.validate_on_submit():

        #Attempting to find existing supervisor --> TO DO: check if this can be implemented more efficiently
        existing_supervisor = SupervisorStudentRanking.query.filter_by(supervisor=form.supervisor.data).first()
        if existing_supervisor:

            #Update existing supervisor details
            existing_supervisor.course = form.course.data
            existing_supervisor.first_student_choice = form.first_student_choice.data
            existing_supervisor.second_student_choice = form.second_student_choice.data
            existing_supervisor.third_student_choice = form.third_student_choice.data
            existing_supervisor.fourth_student_choice = form.fourth_student_choice.data
            existing_supervisor.fifth_student_choice = form.fifth_student_choice.data
            existing_supervisor.capacity = form.capacity.data
        else:
            #Creating new supervisor record if it does not exist yet
            new_supervisor = SupervisorStudentRanking(
                supervisor=form.supervisor.data,
                course=form.course.data,
                first_student_choice=form.first_student_choice.data,
                second_student_choice=form.second_student_choice.data,
                third_student_choice=form.third_student_choice.data,
                fourth_student_choice=form.fourth_student_choice.data,
                fifth_student_choice=form.fifth_student_choice.data,
                capacity=form.capacity.data
            )
            db.session.add(new_supervisor)
        
        db.session.commit()
        flash('Thank you! Your ranking has been submitted. Your final student allocation will be published shortly.')
        return redirect(url_for('home'))
    
    else:
        # Render the form template with error messages
        return render_template('supervisorform.html', title='Supervisors: Student Ranking', form=form)



#run Matching and return output as table
@app.route('/match', methods=['GET', 'POST'])
def match():
    if request.method == 'POST':
        # Clearing old matches
        Match.query.delete()
        db.session.commit()

        # Performing matching process
        matches = perform_matching()

        # Creating new Match objects for each pairing
        for supervisor_ranking_id, student_number in matches.items():
            new_match = Match(student_number=student_number, supervisor_ranking_id=supervisor_ranking_id)
            db.session.add(new_match)
        db.session.commit()

        flash('Matching process completed successfully.')

        # Reloading page to view match list
        return redirect(url_for('match'))

    # Fetching all matches and join with other tables for detailed information in output
    all_matches = db.session.query(
        Match,
        StudentCourseChoice.name.label('student_name'),
        SupervisorStudentRanking.course.label('course_number'),
        SupervisorStudentRanking.supervisor.label('supervisor_name')
    ).join(
        StudentCourseChoice, StudentCourseChoice.student_number == Match.student_number
    ).join(
        SupervisorStudentRanking, SupervisorStudentRanking.id == Match.supervisor_ranking_id
    ).all()

    # Including course titles
    detailed_matches = []
    for match, student_name, course_number, supervisor_name in all_matches:
        # Getting course name from the database
        course = Course.query.get(course_number)
        if course:
            course_title = course.name
        else:
            course_title = "Unknown Course"
        
        detailed_matches.append({
            'match_id': match.id,
            'student_name': student_name,
            'student_number': match.student_number,
            'course_number': course_number,
            'course_title': course_title,
            'supervisor_name': supervisor_name
        })

    return render_template('match.html', matches=detailed_matches)

#Admin Route to choose scenarios
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    form = ConfigForm()

    if request.method == 'POST' and form.validate_on_submit():
        # Retrieve the configuration item for 'active_scenario'
        config = Configuration.query.filter_by(key='active_scenario').first()
        if config:
            # Update the value with the one selected in the form
            config.value = form.configuration.data
            db.session.commit()
            flash('Configuration updated successfully.')
        else:
            # Optionally, create a new configuration record if it doesn't exist
            new_config = Configuration(key='active_scenario', value=form.configuration.data)
            db.session.add(new_config)
            db.session.commit()
            flash('New configuration setting created successfully.')
        
        return redirect(url_for('admin'))

    return render_template('admin.html', form=form)