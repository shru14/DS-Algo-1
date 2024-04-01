from flaskapp.models import StudentCourseChoice, SupervisorStudentRanking

#Fetch Preferences from SQLite Database
def perform_matching():
    # Fetching student preferences from SQLite Database
    student_preferences = {}
    students = StudentCourseChoice.query.all()
    for student in students:
        student_preferences[student.id] = [
            student.first_course_choice, 
            student.second_course_choice, 
            student.third_course_choice, 
            student.fourth_course_choice, 
            student.fifth_course_choice
        ]

    # Fetch supervisor preferences from SQLite Database
    supervisor_preferences = {}
    supervisors = SupervisorStudentRanking.query.all()
    for supervisor in supervisors:
        supervisor_preferences[supervisor.id] = [
            supervisor.first_student_choice, 
            supervisor.second_student_choice, 
            supervisor.third_student_choice, 
            supervisor.fourth_student_choice, 
            supervisor.fifth_student_choice
        ]

    #Execute GS Matching 
    matches = gs_match(student_preferences, supervisor_preferences)
    return matches


#Implementation for simple model of GS (5x5) preference list
#Adjusted object names to the ones used in this flask app implementation
def gs_match(student_preferences, supervisor_preferences):

    matches = {}  # Initatiate dictionary that in the returns all stable matches. Initiated as empty, since we don't have any yet.
    free_students = list(student_preferences.keys()) # Initiate the student as free. Returns the keys from matching dictionary and transforms to list. 
    
    while free_students:
        student = free_students.pop(0) # .pop takes and removes the student at index 0 from the free students list. Assign to student, this equals S in the lecture.
        prof = student_preferences[student].pop(0) # Take the first preference of the first student. This is a professor, as it draws from the student preferences dictionary.
        
        current_match = matches.get(prof) # Assign the 'current match' to a variable to check if professor is currently matched. Current match is a professor.
        # In first iteration, this is always NOT, as the matches dictionary was initiated as empty.
        
        if not current_match: # In case match does not exist yet.
            matches[prof] = student # Match them to each other. Create tentative match, update matches dictionary, as any match is better than the current no match at all.
        else: # If there is a match already:
            prof_pref_list = supervisor_preferences[prof] # If professor is matched otherwise already, get the preferences of the prof. These contain names of students in order of preferences. Assign to variable.
            if prof_pref_list.index(current_match) > prof_pref_list.index(student): # Check if the current match is higher than the current student, which was defined before and is free. Higher, as in index further to the right, so less preferable. 
                matches[prof] = student # Final match, outcome of comparison, match and add prof with student.
                free_students.append(current_match) # As new student is preferred over current match, current match is free again and appended to free list.
            else:
                free_students.append(student) # Vice versa of above.


