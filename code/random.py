import pandas as pd
import functions
import random


# Set seed for reproducibility
random.seed(111)

# 1. Random Allocation of Students to Professors

# Call the function from create_data.py to create two lists of students and professors
data = functions.create_df(10, 5)

# Index the list of lists to assign the students and professors.
# This is done, so they can be individually used as input within the arguments of the random allocater function.
students = data[0]
profs = data[1]

# Use the created lists of students and professors to create a randomly allocated assignment.
first_assignment = functions.random_assignment(students, profs, 2)
print(first_assignment)