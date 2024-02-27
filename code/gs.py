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

