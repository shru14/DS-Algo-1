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


# Now, try to implement a basic gale/shapley allocation based on the dictionries of preferences. This uses the list of lists as input and matches according to the above create set of preferences for both parties.

# Disclaimer: first parts I succeeded to do by myself and with the pseudocode from the lecture, afterwards, I had to be aided extensively by our lord and savior, ChatGPT 
def gs_match(students_preferences, prof_preferences):
    matches = {}
    
    free_student = list(students_preferences.keys()) # Initiate the student as free. Returns the keys from matching dictionary and transfomrs to list.
    
    while free_student:
        student = free_student.pop(0) # .pop takes and removes the students at index 0 from the free students list. 
        prof = students_preferences[student].pop(0) # Take the first preference of the first student.
        
        current_match = matches.get(prof) # Assign the 'current match' to a variable to check if professor is currently matched. Current match is a professor.
        
        if not current_match:
            matches[prof] = student # If not, match them to each other. Create tentative match, update matches dictionary, as a match is better than the current no match at all.
        else:
            prof_pref_list = prof_preferences[prof] # If professor is matched otherwise already, get the preferences of the prof. These contain names of students in order of preferences. Assign to variable.
            if prof_pref_list.index(current_match) > prof_pref_list.index(student): # Check if the current match is higher than the current student, which was defined before and is free.
                matches[prof] = student
                free_student.append(current_match) # As current students is preferred over current match, current student is free again and appended to free list.
            else:
                free_student.append(student)
    return matches


pairs = gs_match(students_preferences = student_pref, prof_preferences = prof_pref)
print(pairs)

# Either run with defined set student_pref as above or pull from "data" (create_data output)
