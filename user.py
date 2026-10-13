"""Abstract User class and concrete Student and Mentor classes."""

import logging
from abc import ABC, abstractmethod

if __package__:
    from .validators import require_identifier, require_text
else:
    from validators import require_identifier, require_text

logger = logging.getLogger(__name__)


class User(ABC):
    """Abstract parent containing properties shared by platform users."""

    _total_users = 0

    def __init__(self, user_id: str | int, name: str, email: str) -> None:
        logger.debug(
            f"Creating user: user_id={user_id!r}, name={name!r}, email={email!r}"
        )
        cleaned_email = require_text(email, "email")
        if not self.is_valid_email(cleaned_email):
            logger.warning(f"Invalid email rejected: email={cleaned_email!r}")
            raise ValueError("email address is invalid")

        self._user_id = require_identifier(user_id, "user ID")
        self._name = require_text(name, "name")
        self._email = cleaned_email
        User._total_users += 1
        logger.info(f"User created: user_id={self._user_id!r}")

    @property
    def user_id(self) -> str:
        """Return the read-only user ID."""
        return self._user_id

    @property
    def name(self) -> str:
        """Return the user's name."""
        return self._name

    @property
    def email(self) -> str:
        """Return the user's email address."""
        return self._email

    @staticmethod
    def is_valid_email(email: object) -> bool:
        """Return True for a basic valid-looking email address."""
        if not isinstance(email, str) or email.count("@") != 1:
            return False
        local_part, domain = email.split("@")
        return bool(local_part and "." in domain and not domain.startswith("."))

    @classmethod
    def get_total_users(cls) -> int:
        """Return the total number of successfully created users."""
        return User._total_users

    def common_details(self) -> str:
        """Return details shared by every user role."""
        return (
            f"User ID: {self.user_id}\n"
            f"Name: {self.name}\n"
            f"Email: {self.email}"
        )

    @abstractmethod
    def display_details(self) -> str:
        """Return information appropriate to the concrete user role."""


class Student(User):
    """Platform user who can enroll in courses."""

    def __init__(self, user_id: str | int, name: str, email: str) -> None:
        super().__init__(user_id, name, email)
        self._course_ids: set[str] = set()
        logger.info(f"Student created: user_id={self.user_id!r}")

    @property
    def course_ids(self) -> tuple[str, ...]:
        """Return enrolled course IDs without exposing the mutable set."""
        return tuple(sorted(self._course_ids))

    def enroll_in_course(self, course_id: str | int) -> None:
        """Record a course enrollment for this student."""
        cleaned_id = require_identifier(course_id, "course ID")
        self._course_ids.add(cleaned_id)
        logger.info(
            f"Course recorded for student: student_id={self.user_id!r}, "
            f"course_id={cleaned_id!r}"
        )

    def display_details(self) -> str:
        """Override the abstract method with student-specific output."""
        courses = ", ".join(self.course_ids) if self.course_ids else "None"
        return f"{self.common_details()}\nRole: Student\nCourses: {courses}"


class Mentor(User):
    """Platform user who teaches courses."""

    def __init__(
        self, user_id: str | int, name: str, email: str, expertise: str
    ) -> None:
        validated_expertise = require_text(expertise, "expertise")
        super().__init__(user_id, name, email)
        self._expertise = validated_expertise
        self._course_ids: set[str] = set()
        logger.info(f"Mentor created: user_id={self.user_id!r}")

    @property
    def expertise(self) -> str:
        """Return the mentor's expertise."""
        return self._expertise

    @property
    def course_ids(self) -> tuple[str, ...]:
        """Return assigned course IDs without exposing the mutable set."""
        return tuple(sorted(self._course_ids))

    def assign_course(self, course_id: str | int) -> None:
        """Record a course assigned to this mentor."""
        cleaned_id = require_identifier(course_id, "course ID")
        self._course_ids.add(cleaned_id)
        logger.info(
            f"Course assigned to mentor: mentor_id={self.user_id!r}, "
            f"course_id={cleaned_id!r}"
        )

    def display_details(self) -> str:
        """Override the abstract method with mentor-specific output."""
        courses = ", ".join(self.course_ids) if self.course_ids else "None"
        return (
            f"{self.common_details()}\n"
            f"Role: Mentor\n"
            f"Expertise: {self.expertise}\n"
            f"Courses: {courses}"
        )
