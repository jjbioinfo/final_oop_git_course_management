"""Tests for the Course Management System."""

from collections.abc import Callable

import contextlib
import io
import logging
from pathlib import Path
import tempfile
from unittest.mock import patch

if __package__:
    from .course import Course
    from .enrollment import Enrollment
    from .exceptions import CourseFullError, DuplicateRecordError, RecordNotFoundError
    from .course_management import CourseManagementSystem
    from .user import Mentor, Student, User
    from . import logging_config, main as application
else:
    from course import Course
    from enrollment import Enrollment
    from exceptions import CourseFullError, DuplicateRecordError, RecordNotFoundError
    from course_management import CourseManagementSystem
    from user import Mentor, Student, User
    import logging_config
    import main as application



def assert_raises(
    expected_exception: type[BaseException],
    function: Callable[..., object],
    *arguments: object,
) -> None:
    """Confirm that a function raises the expected exception."""
    try:
        function(*arguments)
    except expected_exception:
        return
    except Exception as error:
        raise AssertionError(
            f"expected {expected_exception.__name__}, got {type(error).__name__}"
        ) from error
    raise AssertionError(f"expected {expected_exception.__name__}")


def create_system(capacity: int = 2) -> tuple[
    CourseManagementSystem, Student, Student, Mentor, Course
]:
    """Create a small registered system for reuse in tests."""
    system = CourseManagementSystem()
    student1 = Student("S1", "Asha", "asha@example.com")
    student2 = Student("S2", "Rahul", "rahul@example.com")
    mentor = Mentor("M1", "Maya", "maya@example.com", "Python")
    for user in (student1, student2, mentor):
        system.register_user(user)
    course = Course("C1", "Python OOP", mentor, 8, capacity)
    system.add_course(course)
    return system, student1, student2, mentor, course


def test_abstraction_and_inheritance() -> None:
    assert_raises(TypeError, User, "U1", "Test", "test@example.com")
    student = Student("S1", "Asha", "asha@example.com")
    mentor = Mentor("M1", "Maya", "maya@example.com", "Python")
    assert isinstance(student, User)
    assert isinstance(mentor, User)


def test_static_and_class_methods() -> None:
    before = User.get_total_users()
    Student("S1", "Asha", "asha@example.com")
    assert User.get_total_users() == before + 1
    assert User.is_valid_email("learner@example.com") is True
    assert User.is_valid_email("invalid-email") is False


def test_polymorphism() -> None:
    users: list[User] = [
        Student("S1", "Asha", "asha@example.com"),
        Mentor("M1", "Maya", "maya@example.com", "Python"),
    ]
    results = [user.display_details() for user in users]
    assert "Role: Student" in results[0]
    assert "Role: Mentor" in results[1]


def test_enrollment_and_encapsulation() -> None:
    system, student, _, mentor, course = create_system()
    enrollment = system.enroll_student(student.user_id, course.course_id)
    assert enrollment.status == "Active"
    assert student.course_ids == ("C1",)
    assert mentor.course_ids == ("C1",)
    assert course.enrollment_count == 1
    enrollment.complete()
    assert enrollment.status == "Completed"
    assert isinstance(system.list_users(), tuple)
    assert isinstance(student.course_ids, tuple)


def test_duplicates_capacity_and_missing_records() -> None:
    system, student1, student2, mentor, course = create_system(capacity=1)
    system.enroll_student(student1.user_id, course.course_id)
    assert_raises(
        DuplicateRecordError,
        system.enroll_student,
        student1.user_id,
        course.course_id,
    )
    assert_raises(
        CourseFullError,
        system.enroll_student,
        student2.user_id,
        course.course_id,
    )
    assert_raises(DuplicateRecordError, system.register_user, mentor)
    assert_raises(RecordNotFoundError, system.enroll_student, "UNKNOWN", "C1")
    assert_raises(RecordNotFoundError, system.enroll_student, "S1", "UNKNOWN")


def test_course_requires_the_registered_mentor_object() -> None:
    """Reject an unregistered mentor even when its ID belongs to another user."""
    system = CourseManagementSystem()
    registered_student = Student("SHARED", "Asha", "asha@example.com")
    unregistered_mentor = Mentor(
        "SHARED", "Maya", "maya@example.com", "Python"
    )
    system.register_user(registered_student)
    course = Course("C1", "Python OOP", unregistered_mentor, 8, 10)
    assert_raises(RecordNotFoundError, system.add_course, course)


def test_invalid_values() -> None:
    assert_raises(ValueError, Student, "", "Asha", "asha@example.com")
    assert_raises(ValueError, Student, "S1", "", "asha@example.com")
    assert_raises(ValueError, Student, "S1", "Asha", "invalid-email")
    mentor = Mentor("M1", "Maya", "maya@example.com", "Python")
    assert_raises(ValueError, Course, "C1", "Python", mentor, 0, 10)
    assert_raises(ValueError, Course, "C1", "Python", mentor, 4, 0)
    assert_raises(TypeError, Course, "C1", "Python", "Maya", 4, 10)



def test_normalized_identifiers() -> None:
    """Integer and padded text IDs resolve to the same canonical records."""
    system = CourseManagementSystem()
    student = Student(1, "Asha", "asha@example.com")
    mentor = Mentor(2, "Maya", "maya@example.com", "Python")
    system.register_user(student)
    system.register_user(mentor)
    course = Course(3, "Python", mentor, 1, 1)
    system.add_course(course)
    enrollment = system.enroll_student(1, " 3 ")
    assert enrollment.student is student
    assert student.course_ids == ("3",)
    assert_raises(DuplicateRecordError, system.enroll_student, " 1 ", 3)
    for invalid in (True, None, [], 1.5):
        assert_raises(TypeError, system.enroll_student, invalid, 3)
    assert_raises(ValueError, system.enroll_student, " ", 3)


def test_email_contract_and_user_count() -> None:
    """Reject malformed input without claiming complete email-standard support."""
    for email in ("a@example.com", "first.last+tag@sub.example.com"):
        assert User.is_valid_email(email)
    before = User.get_total_users()
    for email in (None, 42, "", "a@b.", "a@.com", "a@b..com", "a b@example.com",
                  "a@example-.com", ".a@example.com", "a..b@example.com", "a@@example.com"):
        assert not User.is_valid_email(email)
        error = TypeError if not isinstance(email, str) else ValueError
        assert_raises(error, Student, "S", "Asha", email)
    assert_raises(ValueError, Mentor, "M", "Maya", "maya@example.com", " ")
    assert User.get_total_users() == before


def test_class_factory() -> None:
    student = Student.from_dict({"user_id": "S", "name": "Asha", "email": "asha@example.com"})
    mentor = Mentor.from_dict({"user_id": "M", "name": "Maya", "email": "maya@example.com",
                               "expertise": "Python"})
    assert type(student) is Student
    assert type(mentor) is Mentor
    assert_raises(TypeError, Student.from_dict, None)
    assert_raises(TypeError, Student.from_dict, {"name": "Asha"})
    assert_raises(TypeError, User.from_dict, {"user_id": "U", "name": "Asha", "email": "asha@example.com"})


def test_failed_operations_preserve_state() -> None:
    system, student1, student2, mentor, course = create_system(capacity=1)
    system.enroll_student(student1.user_id, course.course_id)
    before = (system.list_users(), system.list_courses(), system.list_enrollments())
    assert_raises(CourseFullError, system.enroll_student, student2.user_id, course.course_id)
    assert_raises(TypeError, system.enroll_student, mentor.user_id, course.course_id)
    assert_raises(DuplicateRecordError, system.add_course, course)
    assert (system.list_users(), system.list_courses(), system.list_enrollments()) == before
    assert student2.course_ids == ()
    assert course.enrollment_count == 1
    assert_raises(AttributeError, setattr, student1, "user_id", "CHANGED")
    assert_raises(AttributeError, setattr, course, "capacity", 20)
    assert_raises(TypeError, system.register_user, None)
    assert_raises(TypeError, system.add_course, None)


def test_model_boundaries_and_independent_instances() -> None:
    _, student1, student2, mentor, course = create_system()
    student1.enroll_in_course("C1")
    assert student2.course_ids == ()
    for invalid in (True, 1.5, "2", None):
        assert_raises(TypeError, Course, "C", "Python", mentor, 4, invalid)
    for invalid in (0, -1):
        assert_raises(ValueError, Course, "C", "Python", mentor, 4, invalid)
    assert_raises(TypeError, Enrollment, mentor, course)
    assert_raises(TypeError, Enrollment, student1, None)
    enrollment = Enrollment(student1, course)
    enrollment.complete()
    enrollment.complete()
    assert enrollment.status == "Completed"


def test_logging_file_and_console_fallback() -> None:
    """Use temporary files only; verify both successful logging and an I/O failure."""
    with tempfile.TemporaryDirectory() as directory:
        log_file = Path(directory) / "logs" / "test.log"
        logging_config.configure_logging(log_file)
        logging.getLogger(__name__).info("validation marker")
        assert "validation marker" in log_file.read_text()
        captured = io.StringIO()
        with contextlib.redirect_stderr(captured), patch.object(Path, "mkdir", side_effect=OSError("denied")):
            logging_config.configure_logging(log_file)
        assert "continuing with console logging" in captured.getvalue()
    # Close temporary file/stream handlers so this test does not affect later tests.
    for handler in logging.getLogger().handlers[:]:
        handler.close()
        logging.getLogger().removeHandler(handler)
    logging.getLogger().addHandler(logging.NullHandler())


def test_cli_exit_codes() -> None:
    """Successful demo returns zero; expected and unexpected failures return one."""
    captured = io.StringIO()
    with patch.object(application, "configure_logging"), contextlib.redirect_stdout(captured):
        assert application.main() == 0
    assert "Role: Student" in captured.getvalue()
    assert "Role: Mentor" in captured.getvalue()
    assert "Handled correctly: enrollment already exists" in captured.getvalue()
    with patch.object(application, "configure_logging"), \
         patch.object(application, "CourseManagementSystem", side_effect=ValueError("bad input")), \
         contextlib.redirect_stdout(io.StringIO()):
        assert application.main() == 1
    with patch.object(application, "configure_logging", side_effect=RuntimeError("unexpected")), \
         contextlib.redirect_stdout(io.StringIO()):
        assert application.main() == 1


def run_tests() -> int:
    """Run all test groups and return the failure count."""
    # Expected rejection tests should not print alarming tracebacks to beginners.
    logging.getLogger().addHandler(logging.NullHandler())
    tests = [
        test_abstraction_and_inheritance,
        test_static_and_class_methods,
        test_polymorphism,
        test_enrollment_and_encapsulation,
        test_duplicates_capacity_and_missing_records,
        test_course_requires_the_registered_mentor_object,
        test_invalid_values,
        test_normalized_identifiers,
        test_email_contract_and_user_count,
        test_class_factory,
        test_failed_operations_preserve_state,
        test_model_boundaries_and_independent_instances,
        test_logging_file_and_console_fallback,
        test_cli_exit_codes,
    ]
    failures = 0
    for test in tests:
        try:
            test()
            print(f"PASS: {test.__name__}")
        except Exception as error:
            failures += 1
            print(f"FAIL: {test.__name__}: {error}")
    print(f"Ran {len(tests)} test groups; failures={failures}")
    return failures


if __name__ == "__main__":
    raise SystemExit(run_tests())
