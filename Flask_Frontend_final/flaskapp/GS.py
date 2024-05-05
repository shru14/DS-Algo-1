from flaskapp.models import StudentCourseChoice, SupervisorStudentRanking, Configuration
from flask_sqlalchemy import SQLAlchemy


def get_student_preferences():
    #Fetching student preferences mapped to their course choices
    student_preferences = {}
    students = StudentCourseChoice.query.all()
    for student in students:
        student_preferences[student.student_number] = [
            int(choice.split(' - ')[0]) for choice in [
                student.first_course_choice,
                student.second_course_choice,
                student.third_course_choice,
                student.fourth_course_choice,
                student.fifth_course_choice
            ]
        ]
    return student_preferences


def get_supervisor_preferences():
    # Fetching supervisor preferences mapped to their student choices
    supervisor_preferences = {}
    supervisors = SupervisorStudentRanking.query.all()
    for supervisor in supervisors:
        supervisor_preferences[supervisor.id] = [
            int(student) for student in [
                supervisor.first_student_choice,
                supervisor.second_student_choice,
                supervisor.third_student_choice,
                supervisor.fourth_student_choice,
                supervisor.fifth_student_choice
            ]
        ]
    return supervisor_preferences

student_preferences = get_student_preferences()
supervisor_preferences = get_supervisor_preferences()


def perform_matching():
    # Fetch the current active configuration
    current_config = Configuration.query.filter_by(key='configuration').first()

    if current_config.value == 'even_preferences':
        return default_gs_match(student_preferences, supervisor_preferences)
    elif current_config.value == 'limited_capacity':
        return capacity_gs_match(student_preferences, supervisor_preferences)
    elif current_config.value == 'uneven_preferences':
        return uneven_gs_match(student_preferences, supervisor_preferences)    


#Scneario 1: Default GS Match
def default_gs_match(student_preferences, supervisor_preferences):
    matches = {}
    free_students = list(student_preferences.keys())

    while free_students:
        student = free_students.pop(0)
        if not student_preferences[student]:
            continue  

        preferred_course = student_preferences[student].pop(0)
        print(f"Attempting to match Student {student} with Course {preferred_course}")

        if preferred_course not in supervisor_preferences:
            print(f"No supervisor preference found for {preferred_course}.")

            #Checking if student still has preferences left
            if student_preferences[student]:  
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

#Scenario 2: Limited Capacity GS Match
def capacity_gs_match():
    student_preferences = get_student_preferences()
    supervisor_preferences = get_supervisor_preferences()
    prof_capacities = {supervisor_id: 3 for supervisor_id in supervisor_preferences}  

    matches = {}
    prof_matches = {prof: [] for prof in supervisor_preferences}
    unmatched_students = set(student_preferences.keys())

    while unmatched_students:
        student = unmatched_students.pop()
        for prof in student_preferences[student]:
            if len(prof_matches[prof]) < prof_capacities[prof]:
                matches[student] = prof
                prof_matches[prof].append(student)
                break
            else:
                least_pref_student = min(prof_matches[prof], key=lambda x: supervisor_preferences[prof].index(x))
                if supervisor_preferences[prof].index(student) < supervisor_preferences[prof].index(least_pref_student):
                    matches.pop(least_pref_student)
                    prof_matches[prof].remove(least_pref_student)
                    matches[student] = prof
                    prof_matches[prof].append(student)
                    unmatched_students.add(least_pref_student)
    return matches


#Scenario 3: Uneven Preferences GS Match 
def uneven_gs_match():
    student_preferences = get_student_preferences()
    supervisor_preferences = get_supervisor_preferences()

    matches = {}
    prof_matches = {prof: [] for prof in supervisor_preferences}
    unmatched_students = set(student_preferences.keys())

    while unmatched_students:
        student = unmatched_students.pop()
        for prof in student_preferences[student]:
            if prof in supervisor_preferences and len(prof_matches[prof]) < len(supervisor_preferences[prof]):
                if student not in matches:
                    matches[student] = prof
                    prof_matches[prof].append(student)
                    break
                least_preferred_student = prof_matches[prof][-1]
                if supervisor_preferences[prof].index(student) < supervisor_preferences[prof].index(least_preferred_student):
                    matches.pop(least_preferred_student)
                    matches[student] = prof
                    prof_matches[prof].remove(least_preferred_student)
                    prof_matches[prof].append(student)
                    unmatched_students.add(least_preferred_student)

    return matches