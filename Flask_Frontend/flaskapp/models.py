from flaskapp import db

  # Model for storing student course choices
class StudentCourseChoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    student_number = db.Column(db.String(100), nullable=False)
    first_course_choice = db.Column(db.String(50), nullable=False)
    second_course_choice = db.Column(db.String(50), nullable=False)
    third_course_choice = db.Column(db.String(50), nullable=False)
    fourth_course_choice = db.Column(db.String(50), nullable=False)
    fifth_course_choice = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"StudentCourseChoice('{self.name}', '{self.student_number}', '{self.first_course_choice}', '{self.second_course_choice}', '{self.third_course_choice}, '{self.fourth_course_choice}', '{self.fifth_course_choice}')"
    


  # Model for storing supervisor student ranking
class SupervisorStudentRanking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course = db.Column(db.String(100), nullable=False)
    supervisor_name = db.Column(db.String(100), nullable=False)
    first_student_choice = db.Column(db.String(50), nullable=False)
    second_student_choice = db.Column(db.String(50), nullable=False)
    third_student_choice = db.Column(db.String(50), nullable=False)
    fourth_student_choice = db.Column(db.String(50), nullable=False)
    fifth_student_choice = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"SupervisorStudentRanking('{self.course}', '{self.supervisor_name}', '{self.first_student_choice}', '{self.second_student_choice}', '{self.third_student_choice}, '{self.fourth_student_choice}', '{self.fifth_student_choice}')"
    

# Model for storing Matches created by Gale-Shapley
class Match(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student_course_choice.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('supervisor_student_ranking.id'), nullable=False)
    
    def __repr__(self):
        return f"Match('{self.student_id}', '{self.course_id}')"
