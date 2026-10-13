"""Tests for the Course Management System."""

from collections.abc import Callable

from course import Course
from exceptions import CourseFullError, DuplicateRecordError, RecordNotFoundError
from platform import CourseManagementSystem
from user import Mentor, Student, User


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


def run_tests() -> int:
    """Run all test groups and return the failure count."""
    tests = [
        test_abstraction_and_inheritance,
        test_static_and_class_methods,
        test_polymorphism,
        test_enrollment_and_encapsulation,
        test_duplicates_capacity_and_missing_records,
        test_course_requires_the_registered_mentor_object,
        test_invalid_values,
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
