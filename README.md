# Course Management System

A small Python application that registers students and mentors, creates courses,
and tracks enrollments. It demonstrates object-oriented programming (OOP) with
clear comments, input checks, exceptions, logging, and automated tests.

This is a beginner-friendly, in-memory command-line assignment. It runs without
third-party packages. It does not provide a database, website, or login system.

## Quick start

For the prepared local code, run `python main.py` and `python test_course_management.py`
from this folder. For a published copy, install Python 3.10 or newer and Git,
replace the two placeholders with your repository details, then run:

```sh
git clone https://github.com/YOUR_GITHUB_USERNAME/YOUR_REPOSITORY_NAME.git
cd YOUR_REPOSITORY_NAME
python main.py
python test_course_management.py
```

Use `python3` instead of `python` if that is your computer's Python command.
No `pip install` is needed. An existing Python virtual environment is fine.

The demo prints users, courses, active/completed enrollments, and one deliberately
handled duplicate-enrollment error. The tests finish with:

## Features

- Register students and mentors with unique user IDs.
- Create courses with a registered mentor, duration, and capacity.
- Accept string or integer IDs and normalize them consistently.
- Reject missing records, duplicate enrollments, and full courses.
- Mark enrollments completed; repeating completion is harmless.
- Return student- or mentor-specific details through the same method.
- Expose collection snapshots as tuples rather than mutable internal containers.
- Handle expected errors with `try/except` and record events using `logging`.
- Rotate log files and retain console logging if the log file is unavailable.

## Architecture and classes

A **class** defines a kind of object; an **instance** is one particular object.
An **attribute** stores information; a **method** performs an operation.

| File / class | Responsibility |
|---|---|
| `user.py` / `User` | Validate common user fields and require role-specific display behavior |
| `user.py` / `Student` | Hold a student's enrolled course IDs |
| `user.py` / `Mentor` | Hold expertise and assigned course IDs |
| `course.py` / `Course` | Hold course information and enforce enrollment capacity |
| `enrollment.py` / `Enrollment` | Connect a student to a course and track completion |
| `course_management.py` / `CourseManagementSystem` | Coordinate registration, courses, and enrollments |
| `validators.py` | Reuse small text, identifier, and integer checks |
| `exceptions.py` | Define understandable business-error types |
| `logging_config.py` | Configure console and rotating-file logs |
| `main.py` | Run a complete demonstration and handle application failures |
| `test_course_management.py` | Run success, boundary, invalid-input, and failure checks |

The service module was renamed from `platform.py` to `course_management.py` to
avoid hiding Python's own `platform` module. Use the new import shown below.

## Where each required OOP concept appears

| Concept | Meaning | Source example |
|---|---|---|
| Inheritance | Reuse and extend a parent class | `Student(User)` and `Mentor(User)` |
| Encapsulation | Keep state and the rules for accessing it together | Internal `_course_ids`; public read-only `course_ids` property |
| Polymorphism | The same operation can behave differently for different objects | Both roles implement `display_details()`; `main.py` calls it in one loop |
| Abstraction | Expose a required interface while subclasses supply details | `User(ABC)` and `@abstractmethod display_details()` |
| Instance method | Receives a particular object as `self` | `Enrollment.complete()` |
| Static method | Receives no automatic object/class argument | `User.is_valid_email(email)` |
| Class method | Receives the calling class as `cls` | `Student.from_dict(data)` and `Mentor.from_dict(data)` |

`@property` lets a getter be read as `student.name`, without parentheses.
Leading underscores mark internal implementation by convention; they are not a
security barrier. Tuples protect the returned container, not every referenced
object. See [OOP_GUIDE.md](OOP_GUIDE.md) for a simple code-reading walkthrough.

## Usage example

Run this Python code from the project folder:

```python
import logging

from course import Course
from course_management import CourseManagementSystem
from exceptions import CourseManagementError
from logging_config import configure_logging
from user import Mentor, Student

logger = logging.getLogger(__name__)

try:
    configure_logging()
    system = CourseManagementSystem()
    student = Student.from_dict(
        {"user_id": "S101", "name": "Asha", "email": "asha@example.com"}
    )
    mentor = Mentor("M101", "Maya", "maya@example.com", "Python")
    system.register_user(student)
    system.register_user(mentor)

    course = Course("C101", "Python OOP", mentor, duration_weeks=8, capacity=30)
    system.add_course(course)
    enrollment = system.enroll_student("S101", "C101")
    enrollment.complete()
    print(enrollment.display_details())
except (CourseManagementError, TypeError, ValueError) as error:
    logger.error("Could not finish the operation: %s", error)
except Exception:
    logger.exception("Unexpected example failure")
```

Expected output, apart from log messages:

Perform enrollment through `CourseManagementSystem.enroll_student()` so the
student, course, and enrollment records are updated together. Lower-level model
methods are implementation building blocks, not substitutes for that workflow.
A completed enrollment remains in the roster and counts toward capacity; this
project does not implement cancellation or seat reuse.

## Exception handling and logging

An **exception** reports a failed operation. A `try` block runs work that may
fail; an `except` block handles a specified failure. A **logger** records events.

- Models and validators raise `TypeError` or `ValueError` for invalid data.
- Business rules raise `DuplicateRecordError`, `RecordNotFoundError`, or
  `CourseFullError`, all derived from `CourseManagementError`.
- Service operations catch known errors, log them, and re-raise them. They do
  not return a misleading success value.
- `main()` handles known failures and returns exit code 1. Unexpected exceptions
  are logged with a traceback and a generic user message. Success returns 0.
- Small read-only getters do not need repetitive `try/except` blocks; their
  callers handle failures where recovery or reporting is meaningful.

Logs go to the terminal and `logs/course_management.log`. The file rotates at
approximately 1 MB, keeping three backups. If it cannot be opened, a warning is
printed and console logging continues. Generated logs are ignored by Git.

## Tests and validation

```sh
python test_course_management.py
```

The 14 groups cover the required OOP concepts, class factories, numeric/text ID
normalization, malformed and missing inputs, duplicate and capacity rules,
unchanged state after expected failures, independent instances, logging fallback,
and application exit codes. See [VALIDATION.md](VALIDATION.md) for the actual
execution environment and results. GitHub Actions runs the suite on Python 3.10
and 3.13 for pushes and Pull Requests.

## Scope and limitations

This is a tested educational CLI, not a deployed multi-user production service.
Records live in memory and reset on exit. There is no authentication, persistent
storage, concurrent transaction control, or recovery after process failure.
The email check intentionally accepts a conservative ASCII subset; it neither
covers every valid international email format nor proves mailbox ownership.
`User.get_total_users()` counts successful object constructions during this
process, including unregistered objects; it is not a persistent registered-user
count. Registration itself is represented by `system.list_users()`.

For a real deployment, requirements would need to cover persistence, access
control, backups, concurrency, and operational monitoring. The provided tests do
not certify those absent features.

## References

- [Python classes and inheritance](https://docs.python.org/3/tutorial/classes.html)
- [Abstract base classes](https://docs.python.org/3/library/abc.html)
- [Exceptions](https://docs.python.org/3/tutorial/errors.html)
- [Logging](https://docs.python.org/3/howto/logging.html)

No license has been selected for redistribution; public visibility alone does
not grant a software license.