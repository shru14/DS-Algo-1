import random
import gs
import gs_var2
import gs_places


#Generated dummy names from https://catonmat.net/tools/generate-random-names
students = ['A', 'B', 'C', 'D', 'E', 'F']

#students = ['Willis Spicer', 'Darby Luciano', 'Sidney Coble', 'Leonel Goetz', 'Bilal Mansfield',
            #'Lisbeth Spurlock', 'Darien McDowell', 'Doris Heckman', 'Tariq Spivey', 'Erica McCloud']

professors = ['Prof. Varun Pugh', 'Prof. Silvia Mayfield', 'Prof. Jeffery Breeden']

stud_preferences = {}

for student in students:
    stud_preferences[student] = random.sample(professors, k=3)

print(stud_preferences)

prof_preferences = {}

for professor in professors:
    prof_preferences[professor] = random.sample(students, k=6)

print(prof_preferences)

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

third_var = gs_places.gs_match(students_preferences=stud_preferences, prof_preferences=prof_preferences,
                               places=places)

print(third_var)