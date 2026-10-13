# Read the project as a beginner

Start with `main.py` to understand the story, then inspect the individual models.
The demo creates two students, one mentor, two courses, and three enrollments.
One enrollment is completed. An intentional duplicate is caught and explained.

## 1. Inheritance and `super()`

`class Student(User)` means a student is a specialized user. `User` validates and
stores common fields. `super().__init__(...)` reuses that initialization, so each
subclass does not repeat name, ID, and email validation. Mentor adds expertise.

## 2. Abstraction and ABC

`ABC` means Abstract Base Class. `User` supplies shared code and requires a
`display_details()` implementation. `@abstractmethod` marks that requirement.
Python rejects direct construction of an incomplete abstract class. Student and
Mentor supply their own implementations, so they can be instantiated.

## 3. Encapsulation and properties

`self._user_id` stores a value. `@property def user_id(self)` exposes it through
`student.user_id`. There is no public setter, so `student.user_id = "other"`
fails. The underscore is a convention rather than enforced privacy.

A student stores course IDs internally in a set, which avoids duplicate IDs.
The `course_ids` property returns a sorted tuple, an ordered immutable container,
so callers do not receive the internal set itself.

## 4. Polymorphism

In `main.py`, one loop calls `user.display_details()` for both user types.
Python selects the method belonging to that object's class. Students show their
enrollments; mentors also show expertise. The caller need not write one print
implementation for every role.

## 5. Instance, static, and class methods

| Type | Automatic first argument | Project example | Why it fits |
|---|---|---|---|
| Instance | `self`, the object | `enrollment.complete()` | Changes this enrollment's status |
| Static | None | `User.is_valid_email(value)` | Needs only the supplied email |
| Class | `cls`, the calling class | `Student.from_dict(data)` | Constructs the calling subclass |

`self` and `cls` are conventional parameter names. The decorators determine how
Python passes the object or class. In `from_dict`, `cls(**data)` converts named
dictionary fields into constructor arguments and invokes normal validation.
`Student.from_dict` creates a Student; `Mentor.from_dict` creates a Mentor and
therefore also requires expertise.

## 6. Follow an enrollment through the code

1. The system normalizes the supplied IDs, so integer `1` and text `"1"` refer
   to the same identifier.
2. It checks that the student and course exist and that the user is a Student.
3. It rejects an existing student/course pair.
4. The course checks its capacity before adding the student ID.
5. The student records the course ID.
6. An Enrollment connects those two objects and starts with status `Active`.
7. Calling `complete()` changes that enrollment to `Completed`.

A dictionary maps IDs to objects for lookup. The enrollment dictionary uses a
pair `(student_id, course_id)` as its key: this pair identifies the relationship.

## 7. Why both `raise` and `try/except` appear

`raise` reports a broken rule. The caller decides whether to stop or recover.
A duplicate enrollment is an expected business error; a typo in the code may
cause an unexpected programming error. Catching every exception and returning
`None` would hide the difference and can make callers believe work succeeded.

The service logs rejected operations and re-raises. The demonstration catches its
intentional duplicate and continues. The application's outer handler catches
other failures, logs them, and returns a nonzero exit code. `logger.exception`
includes the traceback, which lists the calls leading to an unexpected failure.

## 8. The import branches

`if __package__` selects relative imports when Python loads the module as part of
a package. `from .user import Student` means the current package's user module.
When `python main.py` runs the file directly, the other branch imports sibling
modules through the script directory. Both execution forms are checked locally.

## 9. What the tests prove

Each test supplies controlled inputs and checks an expected result. Some tests
are successful precisely because an invalid operation raises the expected error.
The suite checks that failed enrollments leave the existing records unchanged.
A passing local test is not proof of live deployment security or concurrency.
