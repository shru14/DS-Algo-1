from flaskapp.models import StudentCourseChoice, SupervisorStudentRanking, Configuration
from flask_sqlalchemy import SQLAlchemy
from flaskapp.init_scenario import get_active_configuration

#Modularized functions for easier oversights
#fetching student preferences
def get_student_preferences():
    # Fetching student preferences mapped to their course choices
    student_preferences = {}

    # TO DO: db query could be defined in a separate function but shouldn't be an issue for small db
    students = StudentCourseChoice.query.all()

    for student in students:
        # Exclude None values and split course choices
        choices = [
            int(choice.split(' - ')[0]) for choice in [
                student.first_course_choice,
                student.second_course_choice,
                student.third_course_choice,
                student.fourth_course_choice,
                student.fifth_course_choice
            ] if choice
        ]
        student_preferences[student.student_number] = choices

    print("Fetched student preferences:", student_preferences)

    return student_preferences



def get_supervisor_preferences():
    supervisor_preferences = {}

    supervisors = SupervisorStudentRanking.query.all()

    for supervisor in supervisors:
        supervisor_preferences[supervisor.id] = [
            student_id for student_id in [
                supervisor.first_student_choice,
                supervisor.second_student_choice,
                supervisor.third_student_choice,
                supervisor.fourth_student_choice,
                supervisor.fifth_student_choice
            ] if student_id is not None
        ]

    print("Fetched supervisor preferences:", supervisor_preferences)
    return supervisor_preferences



def get_supervisor_capacities():
    capacities = {}
    supervisors = SupervisorStudentRanking.query.all()
    for supervisor in supervisors:
        capacities[supervisor.id] = supervisor.capacity

    return capacities



#choosing GS implementation according to selected configuration
def perform_matching():
    # Fetching the current active configuration
    active_config = get_active_configuration()
    print("Active configuration:", active_config)

    # Fetching preferences
    student_preferences = get_student_preferences()
    supervisor_preferences = get_supervisor_preferences()

    # Initialize capacities dictionary
    supervisor_capacities = {}

    # Fetching capacities if necessary
    #included print statement for debugging and validation
    if active_config == 'limited_capacities':
        supervisor_capacities = get_supervisor_capacities()
        print("Supervisor capacities:", supervisor_capacities)

    if active_config == 'even_preferences':
        print("Calling gs_even function...")
        matches = gs_even(student_preferences, supervisor_preferences)
    elif active_config == 'limited_capacities':
        print("Calling gs_capacity function...")
        matches = gs_capacity(student_preferences, supervisor_preferences, supervisor_capacities)
    elif active_config == 'uneven_preferences':
        print("Calling gs_uneven function...")
        matches = gs_uneven(student_preferences, supervisor_preferences)
    else:
        # Handling the case where the configuration is not recognized
        matches = {}
    
    print("Matching completed.")
    return matches if isinstance(matches, dict) else {}




#Configuration 1: GS for Even Preferences
def gs_even(student_preferences, supervisor_preferences):
    matches = {} # Initiate dictionary that in the returns all stable matches. Initiated as empty, since we don't have any yet.
    
    free_students = list(student_preferences.keys()) # Initiate the student as free. Returns the keys from matching dictionary and transforms to list. 
    
    while free_students: 
        student = free_students.pop(0) # .pop takes and removes the student at index 0 from the free students list. Assign to student, this equals S in the lecture.
        supervisor = student_preferences[student].pop(0) # Take the first preference of the first student. This is a supervisor, as it draws from the student preferences dictionary.
        
        current_match = matches.get(supervisor) # Assign the 'current match' to a variable to check if supervisor is currently matched. Current match is a supervisor.
        # In first iteration, this is always NOT, as the matches dictionary was initiated as empty.
        
        if not current_match: # In case match does not exist yet.
            matches[supervisor] = student # Match them to each other. Create tentative match, update matches dictionary, as any match is better than the current no match at all.
        else: # If there is a match already:
            supervisor_pref_list = supervisor_preferences[supervisor] # If supervisor is matched otherwise already, get the preferences of the supervisor. These contain names of students in order of preferences. Assign to variable.
            if supervisor_pref_list.index(current_match) > supervisor_pref_list.index(student): # Check if the current match is higher than the current student, which was defined before and is free. Higher, as in index further to the right, so less preferable. 
                matches[supervisor] = student # Final match, outcome of comparison, match and add supervisor with student.
                free_students.append(current_match) # As new student is preferred over current match, current match is free again and appended to free list.
            else:
                free_students.append(student) # Vice versa of above.
    return matches



#Configuration 2: Limited Capacities
#Added print statements for debugging
def gs_capacity(student_preferences, supervisor_preferences, supervisor_capacities):
    matches = {}  # Initialize dictionary to store matches
    supervisor_matches = {supervisor: [] for supervisor in supervisor_preferences}
    unmatched_students = set(student_preferences.keys())
    proposals = {student: 0 for student in student_preferences.keys()}  # Track proposals made by each student

    while unmatched_students:
        student = unmatched_students.pop()  # Select an unmatched student
        student_prefs = student_preferences[student]  # Get preferences of the student
        while proposals[student] < len(student_prefs):
            supervisor = student_prefs[proposals[student]]  # Get the next preferred supervisor

            print(f"Trying to match student {student} with supervisor {supervisor}")
            print("Supervisor matches:", supervisor_matches[supervisor])
            print("Supervisor preferences:", supervisor_preferences.get(supervisor))

            supervisor_prefs = supervisor_preferences[supervisor]

            if supervisor in supervisor_capacities:
                capacity = supervisor_capacities[supervisor]  # Get capacity for the supervisor
                print(f"Capacity for supervisor {supervisor}: {capacity}")
            else:
                print(f"No capacity information found for supervisor {supervisor}")
                raise ValueError(f"No capacity information found for supervisor {supervisor}")

            if len(supervisor_matches[supervisor]) < capacity:
                # Match the student with the supervisor
                matches[student] = supervisor
                supervisor_matches[supervisor].append(student)
                break
            else:
                least_pref_student = min(supervisor_matches[supervisor], key=lambda x: supervisor_prefs.index(x))
                print("Least preferred student:", least_pref_student)
                print("Supervisor preferences index:", supervisor_prefs.index(least_pref_student))
                if supervisor_prefs.index(student) < supervisor_prefs.index(least_pref_student):
                    # Reject the least preferred student and match the new student
                    matches.pop(least_pref_student)
                    supervisor_matches[supervisor].remove(least_pref_student)
                    matches[student] = supervisor
                    supervisor_matches[supervisor].append(student)
                    unmatched_students.add(least_pref_student)  # Add the rejected student back to unmatched
                    break
            proposals[student] += 1  # Move to the next preference

    return matches




#Configuration 3: Uneven Preferences
#Added print statements for debugging
def gs_uneven(student_preferences, supervisor_preferences):
    matches = {}  # Initialize dictionary to store matches

    # Initialize a dictionary to store the current matches for each supervisor
    supervisor_matches = {supervisor: [] for supervisor in supervisor_preferences}

    # Initialize a set of unmatched students
    unmatched_students = set(student_preferences.keys())

    while unmatched_students:
        student = unmatched_students.pop()  # Select an unmatched student
        student_prefs = student_preferences[student]  # Get preferences of the student

        print(f"Matching student {student}...")

        # Iterate over the student's preferences
        for supervisor in student_prefs:
            supervisor_prefs = supervisor_preferences[supervisor]

            print(f"Checking supervisor {supervisor} preferences:", supervisor_prefs)

            # Check if the supervisor has capacity for more students
            if len(supervisor_matches[supervisor]) < len(supervisor_prefs):
                print(f"Supervisor {supervisor} has capacity for more students.")

                # Match the student with the supervisor
                matches[student] = supervisor
                supervisor_matches[supervisor].append(student)
                print(f"Student {student} matched with supervisor {supervisor}.")
                break
            else:
                # Check if the student is preferred over the least preferred student
                least_preferred_student = supervisor_matches[supervisor][-1]
                print(f"Least preferred student for supervisor {supervisor}: {least_preferred_student}")

                if supervisor_prefs.index(student) < supervisor_prefs.index(least_preferred_student):
                    print(f"Student {student} is preferred over {least_preferred_student} for supervisor {supervisor}.")

                    # Unmatch the least preferred student and match the current student
                    matches.pop(least_preferred_student)
                    matches[student] = supervisor
                    supervisor_matches[supervisor].remove(least_preferred_student)
                    supervisor_matches[supervisor].append(student)
                    unmatched_students.add(least_preferred_student)
                    print(f"Student {student} matched with supervisor {supervisor}.")
                    break
                else:
                    print(f"Student {student} is not preferred over {least_preferred_student} for supervisor {supervisor}.")
                    print("Moving to the next preference.")

    print("Matching completed.")
    return matches
