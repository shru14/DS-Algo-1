def gs_match(students_preferences, prof_preferences, places):
    matches = {}
    remaining_places = places.copy() #Copying places here

    free_student = list(
        students_preferences.keys())  # Initiate the student as free. Returns the keys from matching dictionary and transforms to list.

    while free_student:
        student = free_student.pop(
            0)  # .pop takes and removes the student at index 0 from the free students list. Assign to student, this equals S in the lecture.
        if students_preferences[student]:
            prof = students_preferences[student].pop(
                0)  # Take the first preference of the first student. This is a professor, as it draws from the student preferences dictionary.
            if prof not in matches:
                matches[prof] = [student]
                remaining_places[prof] -= 1
            elif remaining_places[prof] > 0:
                matches[prof].append(student)
                remaining_places[prof] -= 1
            else:
                prof_pref_list = prof_preferences[
                    prof]  # If professor is matched otherwise already, get the preferences of the prof. These contain names of students in order of preferences. Assign to variable.
                current_match = matches[prof][0]

                if prof_pref_list.index(current_match) > prof_pref_list.index(student) and remaining_places[prof] >0:
                    # Check if the current match is higher than the current student, which was defined before and is free. Higher, as in index further to the right, so less preferable.
                    matches[prof] = student  # Final match, outcome of comparison, match and add prof with student.
                    free_student.append(
                        current_match)  # As new student is preferred over current match, current match is free again and appended to free list.
                    remaining_places[prof] =-1
                else:
                    free_student.append(student)  # Vice versa of above.
        else:
            continue
    return matches

student_pref = {
    'A': ['a', 'b', 'c'],
    'B': ['a', 'c', 'b'],
    'C': ['b', 'a', 'c']
}

prof_pref = {
    'a': ['B', 'A', 'C'],
    'b': ['A', 'C', 'B'],
    'c': ['C', 'B', 'A'],
    'd': []
}

place = {
    'a': 3,
    'b': 2,
    'c': 2
}

matches = gs_match(students_preferences=student_pref, prof_preferences=prof_pref, places=place)
print(matches)

