"""Course model for the Course Management System."""

import logging

if __package__:
    from .exceptions import CourseFullError, DuplicateRecordError
    from .user import Mentor, Student
    from .validators import require_identifier, require_positive_integer, require_text
else:
    from exceptions import CourseFullError, DuplicateRecordError
    from user import Mentor, Student
    from validators import require_identifier, require_positive_integer, require_text

logger = logging.getLogger(__name__)


class Course:
    """Represent a course taught by a mentor."""

    def __init__(
        self,
        course_id: str | int,
        title: str,
        mentor: Mentor,
        duration_weeks: int,
        capacity: int,
    ) -> None:
        if not isinstance(mentor, Mentor):
            raise TypeError("mentor must be a Mentor object")
        self._course_id = require_identifier(course_id, "course ID")
        self._title = require_text(title, "title")
        self._mentor = mentor
        self._duration_weeks = require_positive_integer(
            duration_weeks, "duration in weeks"
        )
        self._capacity = require_positive_integer(capacity, "capacity")
        self._student_ids: set[str] = set()
        logger.info(f"Course created: course_id={self.course_id!r}")

    @property
    def course_id(self) -> str:
        return self._course_id

    @property
    def title(self) -> str:
        return self._title

    @property
    def mentor(self) -> Mentor:
        return self._mentor

    @property
    def duration_weeks(self) -> int:
        return self._duration_weeks

    @property
    def capacity(self) -> int:
        return self._capacity

    @property
    def enrollment_count(self) -> int:
        return len(self._student_ids)

    def enroll_student(self, student: Student) -> None:
        """Add a student while protecting duplicates and course capacity."""
        if not isinstance(student, Student):
            raise TypeError("only a Student object can enroll")
        if student.user_id in self._student_ids:
            raise DuplicateRecordError("student is already enrolled in this course")
        if self.enrollment_count >= self.capacity:
            raise CourseFullError(f"course {self.course_id} is full")
        self._student_ids.add(student.user_id)
        logger.info(
            f"Student added to course: course_id={self.course_id!r}, "
            f"student_id={student.user_id!r}"
        )

    def display_details(self) -> str:
        """Return formatted course information."""
        return (
            f"Course ID: {self.course_id}\n"
            f"Title: {self.title}\n"
            f"Mentor: {self.mentor.name}\n"
            f"Duration: {self.duration_weeks} weeks\n"
            f"Enrollment: {self.enrollment_count}/{self.capacity}"
        )
