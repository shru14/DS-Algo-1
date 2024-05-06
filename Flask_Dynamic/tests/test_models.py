import pytest
from app import create_app, db
from app.models import StudentCourseChoice, SupervisorStudentRanking, Match, Configuration, Course, Student

@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    app = create_app("config.py")
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

def test_student_course_choice_model(app):
    with app.app_context():
        # Create a StudentCourseChoice instance
        student_course_choice = StudentCourseChoice(
            name="John Doe",
            student_number=12345,
            first_course_choice="Math",
            second_course_choice="Science",
            third_course_choice="English",
            fourth_course_choice="History",
            fifth_course_choice="Art"
        )
        db.session.add(student_course_choice)
        db.session.commit()

        # Retrieve the saved instance from the database
        saved_student_course_choice = StudentCourseChoice.query.filter_by(name="John Doe").first()

        # Verify that the retrieved instance matches the original one
        assert saved_student_course_choice.name == "John Doe"
        assert saved_student_course_choice.student_number == 12345
        assert saved_student_course_choice.first_course_choice == "Math"
        assert saved_student_course_choice.second_course_choice == "Science"
        assert saved_student_course_choice.third_course_choice == "English"
        assert saved_student_course_choice.fourth_course_choice == "History"
        assert saved_student_course_choice.fifth_course_choice == "Art"

def test_supervisor_student_ranking_model(app):
    with app.app_context():
        # Create a SupervisorStudentRanking instance
        supervisor_student_ranking = SupervisorStudentRanking(
            supervisor="Dr. Smith",
            course="Math",
            first_student_choice="John Doe",
            second_student_choice="Jane Smith",
            third_student_choice="Mike Johnson",
            fourth_student_choice="Emily Brown",
            fifth_student_choice="Alex Davis",
            capacity=2
        )
        db.session.add(supervisor_student_ranking)
        db.session.commit()

        # Retrieve the saved instance from the database
        saved_supervisor_student_ranking = SupervisorStudentRanking.query.filter_by(supervisor="Dr. Smith").first()

        # Verify that the retrieved instance matches the original one
        assert saved_supervisor_student_ranking.supervisor == "Dr. Smith"
        assert saved_supervisor_student_ranking.course == "Math"
        assert saved_supervisor_student_ranking.first_student_choice == "John Doe"
        assert saved_supervisor_student_ranking.second_student_choice == "Jane Smith"
        assert saved_supervisor_student_ranking.third_student_choice == "Mike Johnson"
        assert saved_supervisor_student_ranking.fourth_student_choice == "Emily Brown"
        assert saved_supervisor_student_ranking.fifth_student_choice == "Alex Davis"
        assert saved_supervisor_student_ranking.capacity == 2

def test_match_model(app):
    with app.app_context():
        # Create a Match instance
        match = Match(
            student_number=12345,
            supervisor_ranking_id=1
        )
        db.session.add(match)
        db.session.commit()

        # Retrieve the saved instance from the database
        saved_match = Match.query.filter_by(student_number=12345).first()

        # Verify that the retrieved instance matches the original one
        assert saved_match.student_number == 12345
        assert saved_match.supervisor_ranking_id == 1

def test_configuration_model(app):
    with app.app_context():
        # Create a Configuration instance
        configuration = Configuration(
            key="key1",
            value="value1"
        )
        db.session.add(configuration)
        db.session.commit()

        # Retrieve the saved instance from the database
        saved_configuration = Configuration.query.filter_by(key="key1").first()

        # Verify that the retrieved instance matches the original one
        assert saved_configuration.key == "key1"
        assert saved_configuration.value == "value1"

def test_course_model(app):
    with app.app_context():
        # Create a Course instance
        course = Course(
            name="Math"
        )
        db.session.add(course)
        db.session.commit()

        # Retrieve the saved instance from the database
        saved_course = Course.query.filter_by(name="Math").first()

        # Verify that the retrieved instance matches the original one
        assert saved_course.name == "Math"

def test_student_model(app):
    with app.app_context():
        # Create a Student instance
        student = Student(
            student_number=12345,
            name="John Doe"
        )
        db.session.add(student)
        db.session.commit()

        # Retrieve the saved instance from the database
        saved_student = Student.query.filter_by(student_number=12345).first()

        # Verify that the retrieved instance matches the original one
        assert saved_student.student_number == 12345
        assert saved_student.name == "John Doe"
