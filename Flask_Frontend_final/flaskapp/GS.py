from flaskapp.models import StudentCourseChoice, SupervisorStudentRanking, Configuration


#TO DO: Adjust perform_matching to fetch correct implementation of GS based on the chosen configuration
def perform_matching():
    # Fetching student preferences from the SQLite Database
    student_preferences = {}
    students = StudentCourseChoice.query.all()
    for student in students:

        #Extracting numerical part of course description before the dash
        student_preferences[student.student_number] = [
            int(choice.split(' - ')[0])  

            for choice in [
                student.first_course_choice,
                student.second_course_choice,
                student.third_course_choice,
                student.fourth_course_choice,
                student.fifth_course_choice
            ]
        ]

    # Fetching supervisor preferences from the SQLite Database
    supervisor_preferences = {}
    supervisors = SupervisorStudentRanking.query.all()
    for supervisor in supervisors:

        #Extracting numerical value which functions as course ID for matching
        course_id = int(supervisor.course.split(' - ')[0])

        supervisor_preferences[course_id] = [
            # Assuming student choices are numerical IDs
            supervisor.first_student_choice,
            supervisor.second_student_choice,
            supervisor.third_student_choice,
            supervisor.fourth_student_choice,
            supervisor.fifth_student_choice
        ]


    #Execute GS Matching 
    matches = gs_match(student_preferences, supervisor_preferences)

    #ensuring matches is dictionary + returning dictionary
    return matches if isinstance(matches, dict) else {}




#Implementation for simple model of GS (5x5) preference list
#Adjusted object names to the ones used in this flask app implementation
def gs_match(student_preferences, supervisor_preferences):
    matches = {}
    free_students = list(student_preferences.keys())

    while free_students:
        student = free_students.pop(0)
        if not student_preferences[student]:
            continue  # Skip if student has no more preferences

        preferred_course = student_preferences[student].pop(0)
        print(f"Attempting to match Student {student} with Course {preferred_course}")

        if preferred_course not in supervisor_preferences:
            print(f"No supervisor preference found for {preferred_course}.")
            if student_preferences[student]:  # Check if student still has preferences left
                free_students.append(student)
            continue
        
        current_match = matches.get(preferred_course)

        if not current_match:
            print(f"{preferred_course} is free. Assigning to Student {student}.")
            matches[preferred_course] = student
        else:
            prof_pref_list = supervisor_preferences[preferred_course]
            try:
                current_match_idx = prof_pref_list.index(current_match)
                new_student_idx = prof_pref_list.index(student)
                if current_match_idx > new_student_idx:
                    print(f"Replacing current match {current_match} with {student} for {preferred_course}.")
                    matches[preferred_course] = student
                    free_students.append(current_match)
                else:
                    print(f"Student {student} not preferred over current match {current_match} for {preferred_course}.")
                    if student_preferences[student]:
                        free_students.append(student)
            except ValueError as e:
                print(f"Error: {e}. Data mismatch in preferences for {preferred_course}.")
                if student_preferences[student]:
                    free_students.append(student)

    return matches
