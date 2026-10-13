"""Custom exceptions for course-management operations."""


class CourseManagementError(Exception):
    """Base exception for expected course-management errors."""


class DuplicateRecordError(CourseManagementError):
    """Raised when a user, course, or enrollment already exists."""


class RecordNotFoundError(CourseManagementError):
    """Raised when a requested record does not exist."""


class CourseFullError(CourseManagementError):
    """Raised when a course has no available enrollment places."""
