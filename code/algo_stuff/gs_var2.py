import pandas as pd
import random
import numpy as np


def stable_matching(student_preferences, prof_preferences):
    tentative_pairs = []
    free_stud = []

    def init_free_stud():
        for student in student_preferences:
            free_stud.append(student)

    init_free_stud()

    while len(free_stud) > 0:
        for student in free_stud:
            for professor in student_preferences[student]:
                taken_match = [pair for pair in tentative_pairs if professor in pair]

                if len(taken_match) == 0:
                    tentative_pairs.append([student, professor])
                    free_stud.remove(student)
                    break

                elif len(taken_match) > 0:
                    current_student = prof_preferences[professor].index(taken_match[0][0])
                    potential_student = prof_preferences[professor].index(student)

                    if current_student > potential_student:
                        free_stud.remove(student)
                        free_stud.append(taken_match[0][0])
                        taken_match[0][0] = student
                        break

    return tentative_pairs

