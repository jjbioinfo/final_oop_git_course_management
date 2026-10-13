"""Service layer coordinating users, courses, and enrollments."""

import logging

if __package__:
    from .course import Course
    from .enrollment import Enrollment
    from .exceptions import CourseManagementError, DuplicateRecordError, RecordNotFoundError
    from .user import Student, User
    from .validators import require_identifier
else:
    from course import Course
    from enrollment import Enrollment
    from exceptions import CourseManagementError, DuplicateRecordError, RecordNotFoundError
    from user import Student, User
    from validators import require_identifier

logger = logging.getLogger(__name__)


class CourseManagementSystem:
    """Manage platform records through a focused public interface."""

    def __init__(self) -> None:
        self._users: dict[str, User] = {}
        self._courses: dict[str, Course] = {}
        self._enrollments: dict[tuple[str, str], Enrollment] = {}

    def register_user(self, user: User) -> None:
        """Register a student or mentor with a unique ID."""
        try:
            if not isinstance(user, User):
                raise TypeError("user must inherit from User")
            if user.user_id in self._users:
                raise DuplicateRecordError(f"user ID {user.user_id} already exists")
            self._users[user.user_id] = user
            logger.info(f"User registered: user_id={user.user_id!r}")
        except (CourseManagementError, TypeError, ValueError) as error:
            logger.warning("Course-management operation rejected: %s", error)
            raise  # Keep the exception available to the CLI or another caller.

    def add_course(self, course: Course) -> None:
        """Add a course whose mentor is already registered."""
        try:
            if not isinstance(course, Course):
                raise TypeError("course must be a Course object")
            if course.course_id in self._courses:
                raise DuplicateRecordError(
                    f"course ID {course.course_id} already exists"
                )
            registered_mentor = self._users.get(course.mentor.user_id)
            if registered_mentor is not course.mentor:
                raise RecordNotFoundError("course mentor must be registered first")
            self._courses[course.course_id] = course
            course.mentor.assign_course(course.course_id)
            logger.info(f"Course added: course_id={course.course_id!r}")
        except (CourseManagementError, TypeError, ValueError) as error:
            logger.warning("Course-management operation rejected: %s", error)
            raise  # Keep the exception available to the CLI or another caller.

    def enroll_student(self, student_id: str | int, course_id: str | int) -> Enrollment:
        """Enroll a registered student in an existing course."""
        try:
            # Constructors normalize IDs to strings. Lookups must do the same.
            student_id = require_identifier(student_id, "student ID")
            course_id = require_identifier(course_id, "course ID")
            if student_id not in self._users:
                raise RecordNotFoundError(f"student ID {student_id} was not found")
            if course_id not in self._courses:
                raise RecordNotFoundError(f"course ID {course_id} was not found")

            student = self._users[student_id]
            if not isinstance(student, Student):
                raise TypeError("the supplied user ID does not belong to a student")
            enrollment_key = (student_id, course_id)
            if enrollment_key in self._enrollments:
                raise DuplicateRecordError("enrollment already exists")

            course = self._courses[course_id]
            course.enroll_student(student)
            student.enroll_in_course(course_id)
            enrollment = Enrollment(student, course)
            self._enrollments[enrollment_key] = enrollment
            return enrollment
        except (CourseManagementError, TypeError, ValueError) as error:
            logger.warning("Course-management operation rejected: %s", error)
            raise  # Keep the exception available to the CLI or another caller.

    def list_users(self) -> tuple[User, ...]:
        """Return registered users without exposing the internal dictionary."""
        return tuple(self._users.values())

    def list_courses(self) -> tuple[Course, ...]:
        """Return courses without exposing the internal dictionary."""
        return tuple(self._courses.values())

    def list_enrollments(self) -> tuple[Enrollment, ...]:
        """Return enrollments without exposing the internal dictionary."""
        return tuple(self._enrollments.values())
