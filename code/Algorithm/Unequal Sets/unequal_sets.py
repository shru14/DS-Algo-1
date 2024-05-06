def gs_match(students_preferences, prof_preferences):
    matches = {}  # Initialize dictionary to store matches

    # Initialize a set of unmatched students
    unmatched_students = set(students_preferences.keys())

    while unmatched_students:
        student = unmatched_students.pop()  # Select an unmatched student
        student_prefs = students_preferences[student]  # Get preferences of the student

        # Iterate over the student's preferences
        for prof in student_prefs:
            if prof in matches:  # Check if the professor is already matched
                current_match = matches[prof]
                prof_prefs = prof_preferences[prof]

                # Check if the student is preferred over the current match
                if prof_prefs.index(student) < prof_prefs.index(current_match):
                    # Add the current match back to the pool of unmatched students
                    unmatched_students.add(current_match)
                    # Update the match for the professor
                    matches[prof] = student
                    break
            else:
                # If the professor is not matched, match the student to the professor
                matches[prof] = student
                break

    return matches


stud = {'a': ['A', 'B', 'C'],
        'b': ['C', 'A', 'B'],
        'c': ['A', 'C', 'B'],
        'd': ['C', 'A', 'B'],
        'e': ['A', 'C', 'B']}

prof = {'A': ['a', 'c', 'b', 'e', 'd'],
        'B': ['b', 'd', 'e', 'a', 'c'],
        'C': ['a', 'c', 'd', 'b', 'e']}

print(gs_match(students_preferences=stud, prof_preferences=prof))
