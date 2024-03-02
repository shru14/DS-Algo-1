import pandas as pd
import functions
import random

# Set seed and create data
random.seed(111)
data = functions.create_df(10, 5)


#2. Gale / Shapley Implementation

# Call the defined 'preferences' function to create a dictionary of randomly assigned "prefernces" of profs for each stundent and vice versa.
# Here, recall that the defined function takes a list of lists as input, so we don't exactly use the same input structure as the random allocator function.
student_preferences = functions.preferences(data)
prof_preferences = functions.preferences(data[::-1])

# Look at the results. It should be of this structure: student_#: [prof_#, prof_#, prof_#] and vice versa for the profs.
print(student_preferences)
print(prof_preferences)


# Now, try to implement a basic gale/shapley allocatorb based on the dictionries of preferences. This uses the list of lists as input and matches according to the above create set of preferences for both parties.

print("I don't know this one yet lmao")
print("We'll find out haha")
#Firstly, we are creating an empty list of tentative pairs
tentative_pairs = []
#Also, creating list of students not allocated to professors
free_stud = []
#The function below will append list of free students (not allocated to professors)
def init_free_stud():
    for student in student_preferences:
        free_stud.append(student)

def stable_matching():
    while(len(free_stud) > 0):
        for student in free_stud:
            start_matching(student)
#This function starts matching
def start_matching(student):
    for professor in student_preferences[student]:
#We are checking with this line of code whether match has been created or not by this fancy line of code - not mine, unfortunately :(
#So taken_match can create empty list if professor is free or list of values if professor is already in preference of other student
#But in fact taken_match is boolean for us - empty or not
        taken_match = [pair for pair in tentative_pairs if professor in pair]
#So, if taken_match is empty first iteration creates tentative pairs
        if (len(taken_match) == 0): #it means that if professor is free, it matches under student's preference
            tentative_pairs.append([student, professor])
            free_stud.remove(student)
            break
#Otherwise, as required by the Gale and Shapley algorithm, we are checking professors preferences
        elif (len(taken_match) > 0):
#Now we need to compare rankings of student what tentatively chosen with other option
            current_student = prof_preferences[professor].index(taken_match[0][0])

            potential_student = prof_preferences[professor].index(student)

            if (current_student > potential_student):
#Current student is matched with professor and removed from list of free students
                free_stud.remove(student)

                free_stud.append(taken_match[0][0])
#Again adding to the list to iterate again
                taken_match[0][0] = student
                break

def stable_matching():
    while (len(free_stud) > 0):
        for student in free_stud:
            start_matching(student)


def main():
    init_free_stud():
    print("List of students:" free_stud)
    stable_matching()
    print("List of Matched Pairs:" tentative_pairs)







