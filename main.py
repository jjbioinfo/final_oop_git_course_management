"""Demonstrate the complete Course Management System."""

import logging

if __package__:
    from .course import Course
    from .exceptions import CourseManagementError
    from .logging_config import configure_logging
    from .platform import CourseManagementSystem
    from .user import Mentor, Student, User
else:
    from course import Course
    from exceptions import CourseManagementError
    from logging_config import configure_logging
    from platform import CourseManagementSystem
    from user import Mentor, Student, User

logger = logging.getLogger(__name__)


def main() -> int:
    """Create sample records and demonstrate every major operation."""
    configure_logging()
    logger.info(f"Course Management System started")

    try:
        system = CourseManagementSystem()

        student1 = Student("S101", "Asha", "asha@example.com")
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

        logger.info(f"Course Management System demonstration completed")
        return 0
    except (CourseManagementError, TypeError, ValueError) as error:
        logger.error(f"Course-management operation failed: {error}", exc_info=True)
        print(f"Operation failed: {error}")
        return 1
    except Exception as error:
        logger.critical(f"Unexpected application failure: {error}", exc_info=True)
        print(f"Application error: {error}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
