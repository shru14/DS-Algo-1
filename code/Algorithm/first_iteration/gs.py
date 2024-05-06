import pandas as pd
import functions
import random

# Set seed and create data
random.seed(111)
data = functions.create_data(10, 10)


#2. Gale / Shapley Implementation

# Call the defined 'preferences' function to create a dictionary of randomly assigned "prefernces" of profs for each stundent and vice versa.
# Here, recall that the defined function takes a list of lists as input, so we don't exactly use the same input structure as the random allocator function.
student_preferences = functions.preferences(data)
prof_preferences = functions.preferences(data[::-1])

# Look at the results. It should be of this structure: student_#: [prof_#, prof_#, prof_#] and vice versa for the profs.
# print(student_preferences)
# print(prof_preferences)


# Either run with defined sets student_pref and prof_pref as below, or pull from "data" (create_data output).


student_pref = {
    'A': ['a', 'b', 'c'],
    'B': ['a', 'c', 'b'],
    'C': ['b', 'a', 'c']
}

prof_pref = {
    'a': ['B', 'A', 'C'],
    'b': ['A', 'C', 'B'],
    'c': ['C', 'B', 'A']
}


# Now, try to implement a basic gale/shapley allocation based on the dictionries of preferences.
# This uses the list of lists as input and matches according to the above create set of preferences for both parties.



# Disclaimer: first parts I succeeded to do by myself and with the pseudocode from the lecture.
# The second part, the implementation of the Gale/Shapley algorithm, I had to look up and adapt from the internet.

# Most important part: Variables of student and current_match, which are compared to each other.
# If student is better offer, replace current match. Vice versa.


def gs_match(students_preferences, prof_preferences):
    matches = {} # Initatiate dictionary that in the returns all stable matches. Initiated as empty, since we don't have any yet.
    
    free_student = list(students_preferences.keys()) # Initiate the student as free. Returns the keys from matching dictionary and transforms to list. 
    
    while free_student: 
        student = free_student.pop(0) # .pop takes and removes the student at index 0 from the free students list. Assign to student, this equals S in the lecture.
        prof = students_preferences[student].pop(0) # Take the first preference of the first student. This is a professor, as it draws from the student preferences dictionary.
        
        current_match = matches.get(prof) # Assign the 'current match' to a variable to check if professor is currently matched. Current match is a professor.
        # In first iteration, this is always NOT, as the matches dictionary was initiated as empty.
        
        if not current_match: # In case match does not exist yet.
            matches[prof] = student # Match them to each other. Create tentative match, update matches dictionary, as any match is better than the current no match at all.
        else: # If there is a match already:
            prof_pref_list = prof_preferences[prof] # If professor is matched otherwise already, get the preferences of the prof. These contain names of students in order of preferences. Assign to variable.
            if prof_pref_list.index(current_match) > prof_pref_list.index(student): # Check if the current match is higher than the current student, which was defined before and is free. Higher, as in index further to the right, so less preferable. 
                matches[prof] = student # Final match, outcome of comparison, match and add prof with student.
                free_student.append(current_match) # As new student is preferred over current match, current match is free again and appended to free list.
            else:
                free_student.append(student) # Vice versa of above.
    return matches


# Run it on above example, return and print matches.
pairs = gs_match(students_preferences = student_pref, prof_preferences = prof_pref)
print(pairs)