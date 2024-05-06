import random
import sys
import os

sys.path.append(os.path.abspath('../First_Iteration_Random'))
from gs import gs_match as gs1

sys.path.append(os.path.abspath('../Uneven_Preferences'))
from unequal_sets import gs_match as gs2

sys.path.append(os.path.abspath('../Limited_Capacities'))
from gs_professor_spots_better_version import gs_match_spots as gs3



# Testing

# Example 1: EVEN

#eg_1 = gs1(students_preferences=stud_preferences_1, prof_preferences=prof_preferences_1)
#print("Example 1:", eg_1) #correct


# Example 2: UNEVEN

stud_preferences_2 = {
    'Bob': ['1', '2', '3'],
    'Alice': ['3', '2', '1'],
    'Tom': ['2', '1', '3'],
    'Jim': ['1', '3', '2'],
    'Lisa': ['3', '1', '2']
}

prof_preferences_2 = {
    '1': ['Bob', 'Alice', 'Tom', 'Jim', 'Lisa'],
    '2': ['Lisa', 'Jim', 'Tom', 'Alice', 'Bob'],
    '3': ['Tom', 'Alice', 'Lisa', 'Jim', 'Bob'],
}

eg_2 = gs2(students_preferences=stud_preferences_2, prof_preferences=prof_preferences_2)
print("Example 2:", eg_2) #correct


# Example 3: LIMITED

stud_preferences_3 = {
    'Bob': ['1', '2', '3'],
    'Alice': ['3', '2', '1'],
    'Tom': ['2', '1', '3'],
    'Jim': ['1', '3', '2'],
    'Lisa': ['3', '1', '2']
}

prof_preferences_3 = {
    '1': ['Bob', 'Alice', 'Tom', 'Jim', 'Lisa'],
    '2': ['Lisa', 'Jim', 'Tom', 'Alice', 'Bob'],
    '3': ['Tom', 'Alice', 'Lisa', 'Jim', 'Bob'],
}

prof_spots_3 = {
    '1': 1,
    '2': 2,
    '3': 1,
}

eg_3 = gs3(students_preferences=stud_preferences_3, prof_preferences=prof_preferences_3, prof_capacities=prof_spots_3)
print("Example 3:", eg_3) #correct


