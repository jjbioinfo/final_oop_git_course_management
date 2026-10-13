"""Public interface for the Course Management System."""

from .course import Course
from .enrollment import Enrollment
from .logging_config import configure_logging
from .platform import CourseManagementSystem
from .user import Mentor, Student, User

__all__ = [
    "Course",
    "CourseManagementSystem",
    "Enrollment",
    "Mentor",
    "Student",
    "User",
    "configure_logging",
]
