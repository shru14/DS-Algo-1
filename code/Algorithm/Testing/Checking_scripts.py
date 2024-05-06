import random
import sys
import os

#import gs
#import gs_var2
#import gs_places

# 'Checking_scripts.py' is being run from the 'algo_stuff' directory
sys.path.append(os.path.abspath('../../'))
from Limited_Capacities.gs_professor_spots_better_version import gs_match_spots




#Generated dummy names from https://catonmat.net/tools/generate-random-names
students = ['A', 'B', 'C', 'D', 'E', 'F']

#students = ['Willis Spicer', 'Darby Luciano', 'Sidney Coble', 'Leonel Goetz', 'Bilal Mansfield',
            #'Lisbeth Spurlock', 'Darien McDowell', 'Doris Heckman', 'Tariq Spivey', 'Erica McCloud']

professors = ['Prof. Varun Pugh', 'Prof. Silvia Mayfield', 'Prof. Jeffery Breeden']

stud_preferences = {}

for student in students:
    stud_preferences[student] = random.sample(professors, k=3)

#print(stud_preferences)

prof_preferences = {}

for professor in professors:
    prof_preferences[professor] = random.sample(students, k=6)

#print(prof_preferences)

places =  {
    'Prof. Varun Pugh': 3,
    'Prof. Silvia Mayfield': 1,
    'Prof. Jeffery Breeden': 1
}

#pairs = gs.gs_match(students_preferences = stud_preferences, prof_preferences = prof_preferences)

#print(pairs)

#gs_ver2 = StableMatching_v2()

#output_pr = gs_ver2.main(student_preferences=stud_preferences, prof_preferences=prof_preferences)

#print(output_pr)

#sec_var = gs_var2.stable_matching(student_preferences=stud_preferences, prof_preferences=prof_preferences)

#print(sec_var)

#Very confusing since it gives various results :((((
#Now it's clear - Daniel's algorithm is student oriented and Daniyar's is professor-oriented. That's why results are different

#{'Prof. Silvia Mayfield': 'Willis Spicer', 'Prof. Varun Pugh': 'Darby Luciano', 'Prof. Jeffery Breeden': 'Sidney Coble'}
#[['Sidney Coble', 'Prof. Varun Pugh'], ['Darby Luciano', 'Prof. Silvia Mayfield'], ['Willis Spicer', 'Prof. Jeffery Breeden']]

#third_var = gs_places.gs_match(students_preferences=stud_preferences, prof_preferences=prof_preferences, places=places)
#print(third_var)





# Testing

# Generator of examples
stud = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
prof = ['Prof. Pugh', 'Prof. Mayfield', 'Prof. Breeden', 'Prof. Coble']

stud_pref = {}
for student in stud:
    stud_pref[student] = random.sample(prof, k=3)
print(stud_pref)

prof_pref = {}
for professor in prof:
    prof_pref[professor] = random.sample(stud, k=10)
print(prof_pref)


# Example 1: 3 students, 3 professors, everyone ranks everyone

stud_preferences_1 = {
    'A': ['Prof. Pugh', 'Prof. Mayfield', 'Prof. Breeden'],
    'B': ['Prof. Breeden', 'Prof. Pugh', 'Prof. Mayfield'],
    'C': ['Prof. Pugh', 'Prof. Breeden', 'Prof. Mayfield']
}

prof_preferences_1 = {
    'Prof. Pugh': ['B', 'C', 'A'],
    'Prof. Mayfield': ['B', 'C', 'A'],
    'Prof. Breeden': ['C', 'B', 'A']
}

places_1 = {
    'Prof. Pugh': 1,
    'Prof. Mayfield': 1,
    'Prof. Breeden': 1
}

# answer should be:
# Prof. Pugh - C
# Prof. Mayfield - A
# Prof. Breeden - B
# Unmatched: none

eg_1 = gs_match_spots(students_preferences=stud_preferences_1, prof_preferences=prof_preferences_1, prof_capacities=places_1)
print("Example 1:", eg_1) #correct


# Example 2: 5 students, 5 professors, everyone ranks everyone

stud_preferences_2 = {
    'A': ['Prof. Coble', 'Prof. Breeden', 'Prof. Goetz', 'Prof. Mayfield', 'Prof. Pugh'],
    'B': ['Prof. Mayfield', 'Prof. Pugh', 'Prof. Breeden', 'Prof. Coble', 'Prof. Goetz'],
    'C': ['Prof. Breeden', 'Prof. Goetz', 'Prof. Mayfield', 'Prof. Coble', 'Prof. Pugh'],
    'D': ['Prof. Coble', 'Prof. Pugh', 'Prof. Breeden', 'Prof. Goetz', 'Prof. Mayfield'],
    'E': ['Prof. Coble', 'Prof. Mayfield', 'Prof. Pugh', 'Prof. Goetz', 'Prof. Breeden']
}

prof_preferences_2 = {
    'Prof. Pugh': ['C', 'B', 'E', 'A', 'D'],
    'Prof. Mayfield': ['B', 'A', 'E', 'D', 'C'],
    'Prof. Breeden': ['D', 'A', 'E', 'C', 'B'],
    'Prof. Coble': ['D', 'B', 'A', 'E', 'C'],
    'Prof. Goetz': ['B', 'D', 'E', 'C', 'A']
}

places_2 = {
    'Prof. Pugh': 1,
    'Prof. Mayfield': 1,
    'Prof. Breeden': 1,
    'Prof. Coble': 1,
    'Prof. Goetz': 1,
}

# answer should be:
# Prof. Pugh - E
# Prof. Mayfield - B
# Prof. Breeden - A
# Prof. Coble - D
# Prof. Goetz - C
# Unmatched: none

eg_2 = gs_match_spots(students_preferences=stud_preferences_2, prof_preferences=prof_preferences_2, prof_capacities=places_2)
print("Example 2:", eg_2) #correct


# Example 3: 6 students, 5 professors, everyone ranks everyone

stud_preferences_3 = {
    'A': ['Prof. Mayfield', 'Prof. Goetz', 'Prof. Coble', 'Prof. Breeden', 'Prof. Pugh'],
    'B': ['Prof. Mayfield', 'Prof. Pugh', 'Prof. Coble', 'Prof. Goetz', 'Prof. Breeden'],
    'C': ['Prof. Coble', 'Prof. Breeden', 'Prof. Mayfield', 'Prof. Pugh', 'Prof. Goetz'],
    'D': ['Prof. Breeden', 'Prof. Goetz', 'Prof. Mayfield', 'Prof. Pugh', 'Prof. Coble'],
    'E': ['Prof. Breeden', 'Prof. Goetz', 'Prof. Pugh', 'Prof. Coble', 'Prof. Mayfield'],
    'F': ['Prof. Pugh', 'Prof. Mayfield', 'Prof. Goetz', 'Prof. Coble', 'Prof. Breeden']
}

prof_preferences_3 = {
    'Prof. Pugh': ['B', 'E', 'D', 'C', 'A', 'F'],
    'Prof. Mayfield': ['A', 'E', 'C', 'B', 'F', 'D'],
    'Prof. Breeden': ['D', 'C', 'E', 'B', 'F', 'A'],
    'Prof. Coble': ['F', 'B', 'A', 'D', 'C', 'E'],
    'Prof. Goetz': ['A', 'E', 'D', 'B', 'F', 'C']
}

places_3 = {
    'Prof. Pugh': 1,
    'Prof. Mayfield': 1,
    'Prof. Breeden': 1,
    'Prof. Coble': 1,
    'Prof. Goetz': 1
}

# answer should be:
# Prof. Pugh - B
# Prof. Mayfield - A
# Prof. Breeden - D
# Prof. Coble - F
# Prof. Goetz - E
# Unmatched: C

eg_3 = gs_match_spots(students_preferences=stud_preferences_3, prof_preferences=prof_preferences_3, prof_capacities=places_3)
print("Example 3:", eg_3) #correct


# Example 4: 6 students, 5 professors (6 spots), everyone ranks everyone

stud_preferences_4 = {
    'A': ['Prof. Coble', 'Prof. Mayfield', 'Prof. Pugh', 'Prof. Breeden', 'Prof. Goetz'],
    'B': ['Prof. Pugh', 'Prof. Goetz', 'Prof. Mayfield', 'Prof. Coble', 'Prof. Breeden'],
    'C': ['Prof. Coble', 'Prof. Pugh', 'Prof. Mayfield', 'Prof. Breeden', 'Prof. Goetz'],
    'D': ['Prof. Goetz', 'Prof. Pugh', 'Prof. Coble', 'Prof. Breeden', 'Prof. Mayfield'],
    'E': ['Prof. Breeden', 'Prof. Pugh', 'Prof. Coble', 'Prof. Mayfield', 'Prof. Goetz'],
    'F': ['Prof. Mayfield', 'Prof. Breeden', 'Prof. Goetz', 'Prof. Coble', 'Prof. Pugh']
}

prof_preferences_4 = {
    'Prof. Pugh': ['A', 'E', 'B', 'F', 'C', 'D'],
    'Prof. Mayfield': ['A', 'C', 'B', 'D', 'E', 'F'],
    'Prof. Breeden': ['A', 'B', 'E', 'C', 'D', 'F'],
    'Prof. Coble': ['A', 'C', 'B', 'E', 'D', 'F'],
    'Prof. Goetz': ['D', 'E', 'C', 'F', 'A', 'B']
}

places_4 = {
    'Prof. Pugh': 2,
    'Prof. Mayfield': 1,
    'Prof. Breeden': 1,
    'Prof. Coble': 1,
    'Prof. Goetz': 1
}

# answer should be:
# Prof. Pugh - B, C
# Prof. Mayfield - F
# Prof. Breeden - E
# Prof. Coble - A
# Prof. Goetz - D
# Unmatched: none

eg_4 = gs_match_spots(students_preferences=stud_preferences_4, prof_preferences=prof_preferences_4, prof_capacities=places_4)
print("Example 4:", eg_4) #correct


# Example 5: 6 students, 3 professors (4 spots), everyone ranks everyone

stud_preferences_5 = {
    'A': ['Prof. Breeden', 'Prof. Mayfield', 'Prof. Pugh'],
    'B': ['Prof. Pugh', 'Prof. Mayfield', 'Prof. Breeden'],
    'C': ['Prof. Mayfield', 'Prof. Breeden', 'Prof. Pugh'],
    'D': ['Prof. Breeden', 'Prof. Mayfield', 'Prof. Pugh'],
    'E': ['Prof. Mayfield', 'Prof. Pugh', 'Prof. Breeden'],
    'F': ['Prof. Breeden', 'Prof. Mayfield', 'Prof. Pugh']
}

prof_preferences_5 = {
    'Prof. Pugh': ['B', 'E', 'A', 'F', 'C', 'D'],
    'Prof. Mayfield': ['F', 'D', 'B', 'A', 'C', 'E'],
    'Prof. Breeden': ['E', 'F', 'C', 'B', 'A', 'D']
}

places_5 = {
    'Prof. Pugh': 2,
    'Prof. Mayfield': 1,
    'Prof. Breeden': 1,
}

# answer should be:
# Prof. Pugh - B, E
# Prof. Mayfield - D
# Prof. Breeden - F
# Unmatched: A, C

eg_5 = gs_match_spots(students_preferences=stud_preferences_5, prof_preferences=prof_preferences_5, prof_capacities=places_5)
print("Example 5:", eg_5) #correct


# Example 6: 5 students, 5 professors (5 spots), students only rank 3 professors, professors rank everyone

stud_preferences_6 = {
    'A': ['Prof. Goetz', 'Prof. Breeden', 'Prof. Mayfield'],
    'B': ['Prof. Mayfield', 'Prof. Goetz', 'Prof. Pugh'],
    'C': ['Prof. Mayfield', 'Prof. Breeden', 'Prof. Coble'],
    'D': ['Prof. Goetz', 'Prof. Mayfield', 'Prof. Breeden'],
    'E': ['Prof. Pugh', 'Prof. Goetz', 'Prof. Mayfield']
}

prof_preferences_6 = {
    'Prof. Pugh': ['C', 'A', 'E', 'D', 'B'],
    'Prof. Mayfield': ['A', 'E', 'C', 'D', 'B'],
    'Prof. Breeden': ['A', 'B', 'C', 'E', 'D'],
    'Prof. Coble': ['E', 'A', 'C', 'D', 'B'],
    'Prof. Goetz': ['E', 'C', 'D', 'A', 'B']
}

places_6 = {
    'Prof. Pugh': 1,
    'Prof. Mayfield': 1,
    'Prof. Breeden': 1,
    'Prof. Coble': 1,
    'Prof. Goetz': 1
}

# answer should be:
# Prof. Pugh - E
# Prof. Mayfield - C
# Prof. Breeden - A
# Prof. Coble - B
# Prof. Goetz - D
# Unmatched: none

eg_6 = gs_match_spots(students_preferences=stud_preferences_6, prof_preferences=prof_preferences_6, prof_capacities=places_6)
print("Example 6:", eg_6) #correct


# Example 7: 10 students, 4 professors (7 spots), students only rank 3 professors, professors rank everyone

stud_preferences_7 = {
    'A': ['Prof. Coble', 'Prof. Pugh', 'Prof. Mayfield'],
    'B': ['Prof. Coble', 'Prof. Pugh', 'Prof. Mayfield'],
    'C': ['Prof. Mayfield', 'Prof. Pugh', 'Prof. Breeden'],
    'D': ['Prof. Breeden', 'Prof. Mayfield', 'Prof. Pugh'],
    'E': ['Prof. Breeden', 'Prof. Coble', 'Prof. Pugh'],
    'F': ['Prof. Coble', 'Prof. Pugh', 'Prof. Breeden'],
    'G': ['Prof. Breeden', 'Prof. Pugh', 'Prof. Coble'],
    'H': ['Prof. Breeden', 'Prof. Pugh', 'Prof. Coble'],
    'I': ['Prof. Breeden', 'Prof. Coble', 'Prof. Pugh'],
    'J': ['Prof. Coble', 'Prof. Breeden', 'Prof. Pugh']
}

prof_preferences_7 = {
    'Prof. Pugh': ['E', 'F', 'B', 'H', 'A', 'D', 'C', 'G', 'I', 'J'],
    'Prof. Mayfield': ['H', 'D', 'C', 'I', 'J', 'B', 'E', 'F', 'G', 'A'],
    'Prof. Breeden': ['C', 'D', 'E', 'B', 'I', 'H', 'J', 'F', 'A', 'G'],
    'Prof. Coble': ['B', 'I', 'G', 'F', 'A', 'H', 'C', 'E', 'J', 'D']
}

places_7 = {
    'Prof. Pugh': 2,
    'Prof. Mayfield': 2,
    'Prof. Breeden': 2,
    'Prof. Coble': 1,
}

# answer should be:
# several possible stables matches

eg_7 = gs_match_spots(students_preferences=stud_preferences_7, prof_preferences=prof_preferences_7, prof_capacities=places_7)
print("Example 7:", eg_7) #stable


# Example 8: 10 students, 4 professors (7 spots), students and professors only rank 3 options

stud_preferences_8 = {
    'A': ['Prof. Breeden', 'Prof. Pugh', 'Prof. Coble'],
    'B': ['Prof. Mayfield', 'Prof. Coble', 'Prof. Pugh'],
    'C': ['Prof. Coble', 'Prof. Breeden', 'Prof. Pugh'],
    'D': ['Prof. Pugh', 'Prof. Breeden', 'Prof. Mayfield'],
    'E': ['Prof. Pugh', 'Prof. Coble', 'Prof. Mayfield'],
    'F': ['Prof. Breeden', 'Prof. Mayfield', 'Prof. Coble'],
    'G': ['Prof. Coble', 'Prof. Pugh', 'Prof. Breeden'],
    'H': ['Prof. Mayfield', 'Prof. Coble', 'Prof. Pugh'],
    'I': ['Prof. Mayfield', 'Prof. Pugh', 'Prof. Breeden'],
    'J': ['Prof. Pugh', 'Prof. Coble', 'Prof. Mayfield']
}

prof_preferences_8 = {
    'Prof. Pugh': ['B', 'A', 'D'],
    'Prof. Mayfield': ['B', 'C', 'J'],
    'Prof. Breeden': ['B', 'C', 'H'],
    'Prof. Coble': ['E', 'A', 'G']
}

places_8 = {
    'Prof. Pugh': 2,
    'Prof. Mayfield': 2,
    'Prof. Breeden': 2,
    'Prof. Coble': 1,
}

# answer should be:
# Prof. Pugh - E, J
# Prof. Mayfield - B, H
# Prof. Breeden - A, F
# Prof. Coble - C
# Unmatched: D, G, I

#eg_8 = gs_match_spots(students_preferences=stud_preferences_8, prof_preferences=prof_preferences_8, prof_capacities=places_8)
#print("Example 8:", eg_8) #doesnt run
