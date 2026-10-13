"""Enrollment model connecting a Student with a Course."""

import logging

if __package__:
    from .course import Course
    from .user import Student
else:
    from course import Course
    from user import Student

logger = logging.getLogger(__name__)


class Enrollment:
    """Represent one student's enrollment in one course."""

    def __init__(self, student: Student, course: Course) -> None:
        if not isinstance(student, Student):
            raise TypeError("student must be a Student object")
        if not isinstance(course, Course):
            raise TypeError("course must be a Course object")
        self._student = student
        self._course = course
        self._status = "Active"
        logger.info(
            f"Enrollment created: student_id={student.user_id!r}, "
            f"course_id={course.course_id!r}"
        )

    @property
    def student(self) -> Student:
        return self._student

    @property
    def course(self) -> Course:
        return self._course

    @property
    def status(self) -> str:
        return self._status

    def complete(self) -> None:
        """Mark this enrollment as completed."""
        # Repeating complete() is harmless: the final status remains Completed.
        self._status = "Completed"
        logger.info(
            f"Enrollment completed: student_id={self.student.user_id!r}, "
            f"course_id={self.course.course_id!r}"
        )

    def display_details(self) -> str:
        """Return formatted enrollment information."""
        return (
            f"Student: {self.student.name}\n"
            f"Course: {self.course.title}\n"
            f"Status: {self.status}"
        )
