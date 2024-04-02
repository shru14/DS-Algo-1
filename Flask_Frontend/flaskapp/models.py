from flaskapp import db

#Model for storing student course choices
class StudentCourseChoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    student_number = db.Column(db.Integer, nullable=False)
    first_course_choice = db.Column(db.String(50), nullable=False)
    second_course_choice = db.Column(db.String(50), nullable=False)
    third_course_choice = db.Column(db.String(50), nullable=False)
    fourth_course_choice = db.Column(db.String(50), nullable=False)
    fifth_course_choice = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"StudentCourseChoice('{self.id}', '{self.name}', '{self.student_number}', '{self.first_course_choice}', '{self.second_course_choice}', '{self.third_course_choice}, '{self.fourth_course_choice}', '{self.fifth_course_choice}')"
    


#Model for storing supervisor student ranking
class SupervisorStudentRanking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course = db.Column(db.String(100), nullable=False)
    first_student_choice = db.Column(db.String(50), nullable=False)
    second_student_choice = db.Column(db.String(50), nullable=False)
    third_student_choice = db.Column(db.String(50), nullable=False)
    fourth_student_choice = db.Column(db.String(50), nullable=False)
    fifth_student_choice = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"SupervisorStudentRanking('{self.id}', '{self.course}', {self.first_student_choice}', '{self.second_student_choice}', '{self.third_student_choice}, '{self.fourth_student_choice}', '{self.fifth_student_choice}')"
    
#Model for storing matches 
class Match(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_number = db.Column(db.Integer, nullable=False)
    supervisor_ranking_id = db.Column(db.Integer, db.ForeignKey('supervisor_student_ranking.id'), nullable=False) # TO DO: check if i can just store course_id via form input without referencing the foreign key

    def __repr__(self):
        return f"<Match(id={self.id}, Student Number={self.student_number}, Supervisor Ranking ID={self.supervisor_ranking_id})>"