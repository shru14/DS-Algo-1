def gs_match_all(students_preferences, prof_preferences):
    matches = {}  # Initialize dictionary to store matches

    # Initialize a dictionary to store the current matches for each professor
    prof_matches = {prof: [] for prof in prof_preferences}

    # Initialize a set of unmatched students
    unmatched_students = set(students_preferences.keys())

    while unmatched_students:
        student = unmatched_students.pop()  # Select an unmatched student
        student_prefs = students_preferences[student]  # Get preferences of the student

        # Iterate over the student's preferences
        for prof in student_prefs:
            prof_prefs = prof_preferences[prof]

            # Check if the professor has capacity for more students
            if len(prof_matches[prof]) < len(prof_prefs):
                # Match the student with the professor
                matches[student] = prof
                prof_matches[prof].append(student)
                break
            else:
                # Check if the student is preferred over the least preferred student
                least_preferred_student = prof_matches[prof][-1]
                if prof_prefs.index(student) < prof_prefs.index(least_preferred_student):
                    # Unmatch the least preferred student and match the current student
                    matches.pop(least_preferred_student)
                    matches[student] = prof
                    prof_matches[prof].remove(least_preferred_student)
                    prof_matches[prof].append(student)
                    unmatched_students.add(least_preferred_student)
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

match = gs_match_all(stud, prof)

print(match)