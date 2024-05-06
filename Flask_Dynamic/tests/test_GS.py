import pytest
from app import create_app, db
from app.models import StudentCourseChoice, SupervisorStudentRanking
from unittest.mock import patch
from app.GS import (
    get_student_preferences,
    get_supervisor_preferences,
    get_supervisor_capacities,
    perform_matching,
    gs_even,
    gs_capacity,
    gs_uneven,
)

@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    app = create_app("config.py")
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

def test_get_student_preferences_with_data(app):
    class MockStudentCourseChoice:
        def __init__(self, student_number, first_choice, second_choice, third_choice, fourth_choice, fifth_choice):
            self.student_number = student_number
            self.first_course_choice = first_choice
            self.second_course_choice = second_choice
            self.third_course_choice = third_choice
            self.fourth_course_choice = fourth_choice
            self.fifth_course_choice = fifth_choice

    # Mock data
    student1 = MockStudentCourseChoice("student1", "1 - CourseA", "2 - CourseB", None, None, None)
    student2 = MockStudentCourseChoice("student2", "3 - CourseC", "4 - CourseD", "5 - CourseE", None, None)
    student3 = MockStudentCourseChoice("student3", None, None, None, None, None)

    students = [student1, student2, student3]

    def mock_query_all():
        return students

    with patch("app.models.StudentCourseChoice.query") as mock_query:
        mock_query.all = mock_query_all

        with app.app_context():
            student_preferences = get_student_preferences()

            assert student_preferences == {
                "student1": [1, 2],
                "student2": [3, 4, 5],
                "student3": []
            }


@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    app = create_app("config.py")
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

def test_get_supervisor_preferences_with_data(app):
    class MockSupervisorStudentRanking:
        def __init__(self, supervisor_id, first_choice, second_choice, third_choice, fourth_choice, fifth_choice):
            self.id = supervisor_id
            self.first_student_choice = first_choice
            self.second_student_choice = second_choice
            self.third_student_choice = third_choice
            self.fourth_student_choice = fourth_choice
            self.fifth_student_choice = fifth_choice

    # Mock data
    supervisor1 = MockSupervisorStudentRanking(101, 102, None, None, None, None)
    supervisor2 = MockSupervisorStudentRanking(103, 104, 105, None, None, None)
    supervisor3 = MockSupervisorStudentRanking(106, None, None, None, None, None)

    supervisors = [supervisor1, supervisor2, supervisor3]

    def mock_query_all():
        return supervisors

    with patch("app.models.SupervisorStudentRanking.query") as mock_query:
        mock_query.all = mock_query_all

        with app.app_context():
            supervisor_preferences = get_supervisor_preferences()

            assert supervisor_preferences == {
                101: [102],
                103: [104, 105],
                106: []
            }

def test_get_supervisor_capacities_with_data(app):
    class MockSupervisorStudentRanking:
        def __init__(self, supervisor_id, capacity):
            self.id = supervisor_id
            self.capacity = capacity

    # Mock data
    supervisor1 = MockSupervisorStudentRanking(101, 2)
    supervisor2 = MockSupervisorStudentRanking(103, 3)
    supervisor3 = MockSupervisorStudentRanking(106, None)

    supervisors = [supervisor1, supervisor2, supervisor3]

    def mock_query_all():
        return supervisors

    with patch("app.models.SupervisorStudentRanking.query") as mock_query:
        mock_query.all = mock_query_all

        with app.app_context():
            capacities = get_supervisor_capacities()

            assert capacities == {
                101: 2,
                103: 3,
                106: None
            }



def test_gs_capacity():
    # Define test input
    student_preferences = {
        1: [101, 102],
        2: [101, 102],
        3: [101, 102]
    }
    supervisor_preferences = {
        101: [1, 2, 3],
        102: [3, 2, 1]
    }
    supervisor_capacities = {
        101: 2,
        102: 1
    }

    # Call the matching algorithm
    matches = gs_capacity(student_preferences, supervisor_preferences, supervisor_capacities)

    # Assert the expected output
    assert matches == {
        1: 101,
        2: 101,
        3: 102
    }

def test_gs_uneven():
    # Define test input
    student_preferences = {
        1: [101, 102],
        2: [102, 101]
    }
    supervisor_preferences = {
        101: [1, 2],
        102: [2, 1]
    }

    # Call the matching algorithm
    matches = gs_uneven(student_preferences, supervisor_preferences)

    # Assert the expected output
    assert matches == {
        1: 101,
        2: 102
    }



# Mocking the behavior of internal functions
@pytest.fixture
def mock_matching_functions():
    with patch('app.GS.get_active_configuration', return_value='even_preferences'):
        with patch('app.GS.get_student_preferences', return_value={1: [101, 102], 2: [102, 101]}):
            with patch('app.GS.get_supervisor_preferences', return_value={101: [1, 2], 102: [2, 1]}):
                with patch('app.GS.get_supervisor_capacities', return_value={}):
                    with patch('app.GS.gs_even', return_value={1: 101, 2: 102}):
                        yield

def test_gs_even():
    # Define input data
    student_preferences = {
        1: [101, 102, 103],
        2: [101, 103, 102],
        3: [102, 101, 103]
    }
    supervisor_preferences = {
        101: [1, 2, 3],
        102: [3, 1, 2],
        103: [2, 3, 1]
    }

    # Define expected matches based on the algorithm behavior
    expected_matches = {1: 101, 2: 103, 3: 102}

    # Call the matching algorithm
    matches = gs_even(student_preferences, supervisor_preferences)

    # Assert the expected output
    assert matches == expected_matches


def test_perform_matching(app):
    with app.app_context():
        matches, error_msg = perform_matching()

        assert isinstance(matches, dict)
        assert isinstance(error_msg, (str, type(None)))

        for student, supervisor in matches.items():
            assert isinstance(student, int)
            assert isinstance(supervisor, int)