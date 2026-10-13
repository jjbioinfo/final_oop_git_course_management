# YouTube recording guide (8–10 minutes)

Record your own screen and explanation. This is a script, not a recorded or
uploaded video. After uploading, add the watch URL to `SUBMISSION_LINKS.md`.

## 0:00–0:45: Problem statement

Show the README. Explain: “This project manages students, mentors, courses, and
enrollments. Each Python class has a clear responsibility. This is an in-memory
command-line assignment.” Mention unique IDs, capacity, and duplicate checks.

## 0:45–2:00: Architecture

Show the diagram and file list. User is the common abstract parent. Student and
Mentor specialize it. Course holds course information. Enrollment connects a
student to a course. CourseManagementSystem coordinates those objects.

## 2:00–4:15: All seven OOP requirements

Open `user.py`, `course.py`, and `enrollment.py`:

1. Inheritance: show `Student(User)`, `Mentor(User)`, and `super()`.
2. Abstraction: show `User(ABC)` and `@abstractmethod display_details()`.
3. Encapsulation: show `_course_ids` and the property returning a tuple. Explain
   that an underscore is an internal-use convention, not a security barrier.
4. Polymorphism: show the two display implementations and the common main loop.
5. Instance method: show `Enrollment.complete()` and explain `self`.
6. Static method: show `User.is_valid_email()`; it needs only the supplied value.
7. Class method: show `from_dict()`; `cls(**data)` constructs the calling subclass.

Use `OOP_GUIDE.md` for beginner definitions and the enrollment walkthrough.

## 4:15–5:15: Exceptions and logging

Trace a rejected enrollment in `course_management.py`. Explain how an exception
reports failure, the service logs and re-raises it, and the caller handles it
with `try/except`. Show the expected and unexpected handlers in `main()`.
Show console logging, file rotation, and fallback when the log file is unavailable.

## 5:15–6:30: Execute the program and tests

From the project folder:

```bash
python main.py
python test_course_management.py
```

Explain the two students, one mentor, two courses, three enrollments, completed
status, and deliberately handled duplicate. Show the 14 passing test groups.
Explain that invalid inputs and capacity failures are tested too.
Optionally open `logs/course_management.log` to show recorded events.

## 6:30–8:00: Actual Git and GitHub workflow

```bash
git status --short --branch
git branch --all
git log --oneline --graph --all --decorate
```

Identify the initial commit, `codex/course-validation` feature, its local merge,
and `codex/assignment-submission` Pull Request. Explain commits, branches, and
merges in your own words. Open the real PR from `SUBMISSION_LINKS.md`; show its
diff, commits, automated checks, and merge status. Show the public repository.
Do not reinitialize the repository or replay its original creation commands.

## 8:00–9:00: Final output and limitations

Show the repository and PR links. Explain that no third-party packages are
needed and that records reset at exit. A deployed multi-user system would also
need persistent storage, permissions, and concurrency controls.

## Before submission

- Check readable text, audible narration, and visible execution output.
- Use only fictional data; never show authentication tokens.
- Make the video accessible to the assessor (Public or an accepted Unlisted setting).
- Include the repository and PR links in the YouTube description.
- Put the actual video URL in `SUBMISSION_LINKS.md` and submit all three links.
