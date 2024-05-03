from flask import render_template, flash, redirect, url_for, request, session
from flask import current_app as app
from .extensions import db
from flaskapp.models import StudentCourseChoice, SupervisorStudentRanking, Match, Configuration, Course, Student, db
from flaskapp.studentform import StudentForm
from flaskapp.supervisorform import SupervisorForm
from flaskapp.GS import perform_matching
from flaskapp.models import Configuration
from flaskapp.admin import ConfigForm


#Route for home
@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', title='Course Selection Spring 2024')


#Route for studentform
@app.route('/studentform', methods=['GET', 'POST'])
def studentform():

    #getting current configuration from session, even_preferences set as default
    configuration = session.get('configuration', 'even_preferences') 
    
    #passing current configuration to studentform
    form = StudentForm(configuration=configuration)

    if form.validate_on_submit():
        try:

            #creating new student if not yet in db
            student = Student.query.filter_by(student_number=form.student_number.data).first()
            if not student:
                student = Student(name=form.name.data, student_number=form.student_number.data)
                db.session.add(student)
            
            #creating new course choice if not yet in db
            student_course_choice = StudentCourseChoice.query.filter_by(student_number=form.student_number.data).first()
            if not student_course_choice:
                student_course_choice = StudentCourseChoice(student_number=form.student_number.data)
                db.session.add(student_course_choice)

            #loops over course choices since nr of fields can vary based on dynamic adjustment
            for field_name in form:
                if 'course_choice' in field_name.name:
                    setattr(student_course_choice, field_name.name, field_name.data)

            db.session.commit()
            flash('Thank you! Your course selection has been submitted. Your final course allocation will be published shortly.')
            return redirect(url_for('home'))
        
        #error handling based on form validation 
        except Exception as e:
            flash(f'An error occurred: {str(e)}', 'error')

    return render_template('studentform.html', form=form, title='Student Form')



@app.route('/supervisorform', methods=['GET', 'POST'])
def supervisorform():

    #getting current configuration from session, even_preferences set as default
    configuration = session.get('configuration', 'even_preferences')

    #passing current configuration to supervisorform
    form = SupervisorForm(configuration=configuration)

    if form.validate_on_submit():
        try:
            #creating new SupervisorStudentRanking entry if not yet in db
            supervisor_ranking = SupervisorStudentRanking.query.filter_by(
                supervisor=form.supervisor.data, course=form.course.data).first()
            if not supervisor_ranking:
                supervisor_ranking = SupervisorStudentRanking(
                    supervisor=form.supervisor.data,
                    course=form.course.data)
                db.session.add(supervisor_ranking)

            #Update student choices based on configuration (technically the same in all configurations but want to avoic hardcoding)
            for field_name in ['first_student_choice', 'second_student_choice',
                               'third_student_choice', 'fourth_student_choice', 'fifth_student_choice']:
                if hasattr(form, field_name):
                    setattr(supervisor_ranking, field_name, getattr(form, field_name).data)

            #Updating capacity field if configuration set to limited capacity
            if configuration == 'limited_capacity' and hasattr(form, 'capacity'):
                supervisor_ranking.capacity = form.capacity.data

            db.session.commit()
            flash('Thank you! Your course selection has been submitted. Your final student allocation will be published shortly.')
            return redirect(url_for('home'))
        except Exception as e:
            flash(f'An error occurred: {str(e)}', 'error')
           

    return render_template('supervisorform.html', form=form, title='Supervisor Ranking Form')



#Matching route + returning output as table
@app.route('/match', methods=['GET', 'POST'])
def match():
    if request.method == 'POST':

        #Clearing old matches
        Match.query.delete()
        db.session.commit()

        #matching process (configuration defined in GS.py)
        matches = perform_matching()

        #creating new Match objects 
        for supervisor_ranking_id, student_number in matches.items():
            new_match = Match(student_number=student_number, supervisor_ranking_id=supervisor_ranking_id)
            db.session.add(new_match)
        db.session.commit()

        flash('Matching process completed successfully.')

        #reloading page to view match list
        return redirect(url_for('match'))

    #fetching all matches and joining with other tables for more detailled output
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

    #including course titles
    detailed_matches = []
    for match, student_name, course_number, supervisor_name in all_matches:
      
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


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    form = ConfigForm(request.form)
    if request.method == 'POST' and form.validate():

        #storing configuration in session 
        session['configuration'] = form.configuration.data  

        return redirect(url_for('admin'))  
    return render_template('admin.html', form=form)


#Displaying selected scenario (this is not working atm, the query should be correct though)
@app.context_processor
def inject_configuration():
    current_config = Configuration.query.filter_by(key='configuration').first()
    return {'configuration': current_config}