import random
import gs
import gs_var2



#Generated dummy names from https://catonmat.net/tools/generate-random-names
students = ['Willis Spicer', 'Darby Luciano', 'Sidney Coble']

#students = ['Willis Spicer', 'Darby Luciano', 'Sidney Coble', 'Leonel Goetz', 'Bilal Mansfield',
            #'Lisbeth Spurlock', 'Darien McDowell', 'Doris Heckman', 'Tariq Spivey', 'Erica McCloud']

professors = ['Prof. Varun Pugh', 'Prof. Silvia Mayfield', 'Prof. Jeffery Breeden']

stud_preferences = {}

for student in students:
    stud_preferences[student] = random.sample(professors, k=3)

print(stud_preferences)

prof_preferences = {}

for professor in professors:
    prof_preferences[professor] = random.sample(students, k=3)

print(prof_preferences)

pairs = gs.gs_match(students_preferences = stud_preferences, prof_preferences = prof_preferences)

print(pairs)

#gs_ver2 = StableMatching_v2()

#output_pr = gs_ver2.main(student_preferences=stud_preferences, prof_preferences=prof_preferences)

#print(output_pr)

sec_var = gs_var2.stable_matching(student_preferences=stud_preferences, prof_preferences=prof_preferences)

print(sec_var)

#Very confusing since it gives various results :((((

#{'Prof. Silvia Mayfield': 'Willis Spicer', 'Prof. Varun Pugh': 'Darby Luciano', 'Prof. Jeffery Breeden': 'Sidney Coble'}
#[['Sidney Coble', 'Prof. Varun Pugh'], ['Darby Luciano', 'Prof. Silvia Mayfield'], ['Willis Spicer', 'Prof. Jeffery Breeden']]