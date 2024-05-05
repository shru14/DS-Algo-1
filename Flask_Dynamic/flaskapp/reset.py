#script for resetting entries in SQlite db (preference + match tables)
#reset button could be included in admin panel 


from flaskapp.models import StudentCourseChoice, SupervisorStudentRanking, Match
from flaskapp.extensions import db

#session query to reset entries currently not working

'''
def reset_database_entries():
    try:
        #Deleting all entries from defined tables
        #db.session.query(StudentCourseChoice).delete()
        db.session.query(SupervisorStudentRanking).delete()
        #db.session.query(Match).delete()

        db.session.commit()
        print("Database entries reset successfully.")

    except Exception as e:
        # Rollback the changes if an error occurs
        db.session.rollback()
        print("Error resetting database entries:", str(e))

#Calling the function to reset entries --> could be integrated into a button in admin panel
reset_database_entries()

'''