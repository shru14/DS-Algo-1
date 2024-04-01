from flask import render_template, flash, redirect, url_for, request
from flaskapp import app, db
from flaskapp.models import StudentCourseChoice, SupervisorStudentRanking, Match
from flaskapp.studentform import StudentForm
from flaskapp.supervisorform import SupervisorForm
from flaskapp.GS import perform_matching, gs_match

# Route for the home page, which is where the blog posts will be shown
@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', title='Course Selection Spring 2024')


# Route for the about page
@app.route("/about")
def about():
    return render_template('about.html', title='About page')

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
    return render_template('studentform.html', title='Students: Course Selection', form=form)


#Route for Supervisor page
@app.route("/supervisorform", methods=['GET', 'POST'])
def supervisorform():
    form = SupervisorForm()
    if form.validate_on_submit():
        selection = SupervisorStudentRanking(
            course=form.course.data,
            supervisor_name=form.supervisor_name.data,
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
    return render_template('supervisorform.html', title='Supervisors: Student Ranking', form=form)


@app.route('/matching')
def matching():
    matches = perform_matching()  

    for supervisor_ranking_id, student_number in matches.items():
        
        new_match = Match(student_number=student_number, supervisor_ranking_id=supervisor_ranking_id) #creates new match object for each pairing
        db.session.add(new_match)
    db.session.commit()

    flash('Matching process completed successfully.')
    return redirect(url_for('home'))


#Query Matches 
@app.route('/viewmatches')
def viewmatches():

    # Query all matches
    all_matches = Match.query.all()
    
    match_details = []
    for match in all_matches:
        student = StudentCourseChoice.query.get(match.student_id)

       
        professor = SupervisorStudentRanking.query.filter_by(course=match.course_id).first()

       
        match_details.append({
            'student_name': student.name,
            'student_number': student.student_number,
            'course': match.course_id,  # Or replace with professor.course if that's more appropriate
            'professor_name': professor.supervisor_name if professor else "N/A"  # Handling cases where professor might not be found
        })
    
    return render_template('viewmatches.html', matches=match_details)