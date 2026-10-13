# Video Explanation Guide

## 1. Problem statement

Explain that the project manages students, mentors, courses, and enrollments by
using separate Python classes and modules.

## 2. Architecture

- `User` is the abstract parent class.
- `Student` and `Mentor` inherit from `User`.
- `Course` stores course and mentor information.
- `Enrollment` connects one student to one course.
- `CourseManagementSystem` coordinates all objects.

## 3. OOP concepts

- **Inheritance:** Show `Student(User)` and `Mentor(User)`.
- **Abstraction:** Show `User(ABC)` and the abstract `display_details()` method.
- **Encapsulation:** Show protected attributes such as `_user_id` and their
  read-only properties.
- **Polymorphism:** Show the loop in `main.py` that calls
  `user.display_details()` for both students and mentors.
- **Instance methods:** Demonstrate registering, enrolling, and completing an
  enrollment.
- **Static method:** Demonstrate `User.is_valid_email()`.
- **Class method:** Demonstrate `User.get_total_users()`.

## 4. Git and GitHub workflow

Explain repository initialization, meaningful commits, the
`feature/user-models` and `feature/course-management` branches, the local merge,
the Pull Request, its review and merge, and the final Git history.

## 5. Execution and testing

Run:

```bash
python main.py
python test_course_management.py
```

Explain the displayed users, courses, enrollments, validation failures, and test
results. Finish by showing the public repository URL and Pull Request URL.
