# Course Management System

A modular command-line learning platform built with Python object-oriented
programming. The system manages students, mentors, courses, and enrollments while
demonstrating the principal OOP concepts required by the assignment.

## Features

- Register students and mentors with unique IDs.
- Create courses taught by registered mentors.
- Enroll students while preventing duplicates and over-capacity enrollment.
- Track active and completed enrollments.
- Display role-specific student and mentor information.
- Validate required data and report expected errors clearly.
- Record application activity in `logs/course_management.log`.

## Architecture

```text
User (abstract)
├── Student
└── Mentor

CourseManagementSystem
├── manages User objects
├── manages Course objects
└── creates Enrollment objects

Enrollment
└── connects one Student with one Course
```

### Classes

| Class | Responsibility |
|---|---|
| `User` | Abstract parent containing common user data and behavior |
| `Student` | Stores enrolled courses and student-specific output |
| `Mentor` | Stores expertise and assigned courses |
| `Course` | Stores course details, capacity, mentor, and students |
| `Enrollment` | Represents and updates a student-course relationship |
| `CourseManagementSystem` | Coordinates registration, courses, and enrollment |

## OOP concepts demonstrated

- **Inheritance:** `Student` and `Mentor` inherit from `User`.
- **Abstraction:** `User` inherits from `ABC`; `display_details()` is abstract.
- **Encapsulation:** Internal collections use protected attributes and properties
  return safe immutable tuples.
- **Polymorphism:** The same `user.display_details()` call produces student or
  mentor output according to the runtime object.
- **Instance methods:** Objects register courses, enroll students, and complete
  enrollments.
- **Static method:** `User.is_valid_email()` validates an email without an object.
- **Class method:** `User.get_total_users()` returns the shared user count.

## Requirements

- Python 3.10 or newer
- No third-party Python packages
- Git and GitHub CLI for the repository workflow

## Installation

```bash
git clone YOUR_PUBLIC_REPOSITORY_URL
cd course-management-system
```

No package installation is required.

## Usage

Run the demonstration:

```bash
python main.py
```

Run the test suite:

```bash
python test_course_management.py
```

Example code:

```python
from course import Course
from platform import CourseManagementSystem
from user import Mentor, Student

system = CourseManagementSystem()
student = Student("S101", "Asha", "asha@example.com")
mentor = Mentor("M101", "Maya", "maya@example.com", "Python")

system.register_user(student)
system.register_user(mentor)

course = Course("C101", "Python OOP", mentor, 8, 30)
system.add_course(course)
enrollment = system.enroll_student("S101", "C101")
```

## Git and GitHub workflow

The `git_workflow.sh` file contains an unexecuted workflow that demonstrates:

- Repository initialization
- Feature branches
- Meaningful commits
- A local `--no-ff` merge
- Pushing branches to a public GitHub repository
- Creating and merging a Pull Request
- Viewing the final commit graph

Review the script before running it during the recorded demonstration.
Use [`VIDEO_SCRIPT.md`](VIDEO_SCRIPT.md) as the recording checklist.

## Submission links

- Public GitHub repository: `GENERATED-AFTER-RUNNING-THE-GIT-SCRIPT`
- Pull Request: `GENERATED-AFTER-RUNNING-THE-GIT-SCRIPT`
- YouTube video: `ADD-YOUTUBE-VIDEO-URL`

## Limitations

This learning project stores data in memory. Data is reset when the program ends,
and no real learning platform or payment service is contacted.
