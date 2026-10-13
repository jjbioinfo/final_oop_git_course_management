"""Demonstrate the complete Course Management System."""

import logging

if __package__:
    from .course import Course
    from .exceptions import CourseManagementError
    from .logging_config import configure_logging
    from .course_management import CourseManagementSystem
    from .user import Mentor, Student, User
else:
    from course import Course
    from exceptions import CourseManagementError
    from logging_config import configure_logging
    from course_management import CourseManagementSystem
    from user import Mentor, Student, User

logger = logging.getLogger(__name__)


def main() -> int:
    """Create sample records and demonstrate every major operation."""
    try:
        configure_logging()
        logger.info("Course Management System started")
        system = CourseManagementSystem()

        # A class method constructs the calling class and reuses its validation.
        student1 = Student.from_dict(
            {"user_id": "S101", "name": "Asha", "email": "asha@example.com"}
        )
        student2 = Student("S102", "Rahul", "rahul@example.com")
        mentor = Mentor("M101", "Maya", "maya@example.com", "Python")

        for user in (student1, student2, mentor):
            system.register_user(user)

        python_course = Course("C101", "Python OOP", mentor, 8, 2)
        git_course = Course("C102", "Git and GitHub", mentor, 4, 3)
        system.add_course(python_course)
        system.add_course(git_course)

        enrollment1 = system.enroll_student("S101", "C101")
        system.enroll_student("S102", "C101")
        system.enroll_student("S101", "C102")
        enrollment1.complete()

        print("USERS")
        # Polymorphism: the same call selects the appropriate child implementation.
        for user in system.list_users():
            print(user.display_details())
            print()

        print("COURSES")
        for course in system.list_courses():
            print(course.display_details())
            print()

        print("ENROLLMENTS")
        for enrollment in system.list_enrollments():
            print(enrollment.display_details())
            print()

        print(f"Total users created: {User.get_total_users()}")
        print(f"Valid email example: {User.is_valid_email('learner@example.com')}")

        print("\nEXPECTED ERROR: DUPLICATE ENROLLMENT")
        try:
            system.enroll_student("S101", "C101")
        except CourseManagementError as error:
            # A known business error is shown clearly; the valid records remain intact.
            print(f"Handled correctly: {error}")
            logger.info("Demonstration handled the expected duplicate enrollment")

        logger.info("Course Management System demonstration completed")
        return 0
    except (CourseManagementError, TypeError, ValueError) as error:
        logger.error("Course-management operation failed: %s", error)
        print(f"Operation failed: {error}")
        return 1
    except Exception as error:
        logger.exception("Unexpected application failure")
        print("An unexpected error occurred. See the log for details.")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
