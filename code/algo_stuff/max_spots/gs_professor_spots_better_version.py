def gs_match_spots(students_preferences, prof_preferences, prof_capacities):
    matches = {}  # Initialize dictionary to store matches
    prof_matches = {prof: [] for prof in prof_preferences}
    unmatched_students = set(students_preferences.keys())
    proposals = {student: 0 for student in students_preferences.keys()}  # Track proposals made by each student

    while unmatched_students:
        student = unmatched_students.pop()  # Select an unmatched student
        student_prefs = students_preferences[student]  # Get preferences of the student
        while proposals[student] < len(student_prefs):
            prof = student_prefs[proposals[student]]  # Get the next preferred professor
            prof_prefs = prof_preferences[prof]
            capacity = prof_capacities[prof]  # Get capacity for the professor
            if len(prof_matches[prof]) < capacity:
                # Match the student with the professor
                matches[student] = prof
                prof_matches[prof].append(student)
                break
            else:
                # Check if the student is preferred over the least preferred in the professor's matches
                least_pref_student = min(prof_matches[prof], key=lambda x: prof_prefs.index(x))
                if prof_prefs.index(student) < prof_prefs.index(least_pref_student):
                    # Reject the least preferred student and match the new student
                    matches.pop(least_pref_student)
                    prof_matches[prof].remove(least_pref_student)
                    matches[student] = prof
                    prof_matches[prof].append(student)
                    unmatched_students.add(least_pref_student)  # Add the rejected student back to unmatched
                    break
            proposals[student] += 1  # Move to the next preference

    return matches

stud = {'a': ['A', 'B', 'C'],
        'b': ['C', 'A', 'B'],
        'c': ['A', 'C', 'B'],
        'd': ['C', 'A', 'B'],
        'e': ['A', 'C', 'B']}

prof = {'A': ['a', 'c', 'b', 'e', 'd'],
        'B': ['b', 'd', 'e', 'a', 'c'],
        'C': ['a', 'c', 'd', 'b', 'e']}

spots = {'A': 2,
         'B': 3,
         'C': 1}

match4 = gs_match_spots(stud, prof, spots)

print(match4)