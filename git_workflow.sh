#!/usr/bin/env bash


# ============================================================================
# 1. START RECORDING: INITIALIZE GIT IN THIS SAME FOLDER
# ============================================================================
# SAY: "My Python code is prepared. I will track it in logical feature commits."
# The directory must be the exact project folder shown below.

cd /Users/JJOHN41/Documents/my_learning/euron_super30/assignment/week6/5_final_oop_git_course_management
pwd
# This creates NEW history because Step 0 moved the previous .git directory.
git init --initial-branch=main
# Expected output says "Initialized empty Git repository", NOT "Reinitialized".
# If it says Reinitialized, STOP: the before-recording preparation was not done.

# Replace these values with your own name and commit email before running.
# These settings apply to this repository only.
git config user.name "jjbioinfo"
git config user.email "jibinbioinfo@gmail.com"
  
# Expected root: .../week6/5_final_oop_git_course_management.
git rev-parse --show-toplevel
# Expected: NO remote output. The previous origin is in the backed-up metadata.
git remote -v
 
# Use the existing environment; no third-party package installation is needed.
source /Users/JJOHN41/Documents/my_learning/euron_super30/.venv/bin/activate
python --version

# ============================================================================
# 2. INITIAL COMMIT: VALIDATION, ERRORS, AND LOGGING
# ============================================================================
# SAY: "git add selects files for a snapshot; git commit saves that snapshot."
# .gitignore keeps generated logs and Python caches out of the repository.
# validators.py shares input checks; exceptions.py defines business errors;
# logging_config.py configures console logging and rotating log files.

git add .gitignore validators.py exceptions.py logging_config.py
# Review exactly what is staged before committing.
git diff --cached --stat
git commit -m "Add validation helpers, business exceptions, and logging"
git status --short --branch
# Expected: first commit on main. Other prepared files show ?? (untracked).
# This is normal: you will commit those files in the following feature steps.

# ============================================================================
# 3. MODEL FEATURE: FIVE CLASSES AND OOP CONCEPTS
# ============================================================================
# SAY: "A feature branch lets me develop one part separately from main."
git switch -c codex/oop-models

# Open user.py, course.py, enrollment.py and explain:
# - User(ABC): an abstract parent; @abstractmethod requires role behavior.
# - Student(User), Mentor(User): inheritance; super() calls parent behavior.
# - Properties/internal attributes: encapsulation and controlled access.
# - display_details(): polymorphism, the same method with role-specific output.
# - complete(self): instance method, operates on one enrollment object.
# - @staticmethod is_valid_email: uses supplied data, no automatic self/cls.
# - @classmethod from_dict(cls, data): creates an instance of the calling class.

python -c "from user import User, Student, Mentor; from course import Course; from enrollment import Enrollment; print('Model imports passed')"
# Expected: Model imports passed. Stop and fix any import error before committing.
git add user.py course.py enrollment.py
git diff --cached --stat
git commit -m "Add User, Student, Mentor, Course, and Enrollment models"

# Demonstrate a LOCAL merge; --no-ff preserves a visible merge commit.
git switch main
git merge --no-ff codex/oop-models -m "Merge OOP model feature"
git log --oneline --graph --all --decorate
# SAY: "The model feature is now part of main. The graph records the merge."

# ============================================================================
# 4. SERVICE FEATURE: RUN THE CODE, HANDLE ERRORS, AND TEST
# ============================================================================
git switch -c codex/course-service

# Open course_management.py and main.py. Explain registration, course creation,
# enrollment, try/except, and logger calls. Expected errors are handled; unexpected
# errors are logged with a traceback. Small getters do not need repeated handlers.
python main.py
# Expected: users, courses, enrollments, completion, and a handled duplicate error.
python test_course_management.py
 # Expected final line: Ran 14 test groups; failures=0
# Tests cover normal cases, invalid input, duplicate IDs, capacity, and log failure.
# Commit only after the program and tests complete successfully.

git add course_management.py main.py __init__.py test_course_management.py
git diff --cached --check
git commit -m "Add course service, demo, error handling, and tests"

# ============================================================================
# 5. README AND CI: PREPARE THIS FEATURE FOR A PULL REQUEST
# ============================================================================
# Stay on codex/course-service. The PR will include the service AND these docs.
# Open README.md and update its clone URL/folder to your chosen GitHub repository.
# Use your ACTUAL account and a NEW, UNUSED repository name.
# Remove references to documentation files you chose not to include.
# Explain description, class architecture, installation, features, and examples.
# .github/workflows/tests.yml runs tests on Python 3.10 and 3.13 in GitHub Actions.

git add README.md git_workflow.sh .github/workflows/tests.yml
git diff --cached --check
git diff --cached --stat
git commit -m "Document usage and add automated Python checks"

# Show the two feature commits that will be proposed to main.
git log --oneline main..HEAD
git status --short --branch
# Expected: clean working directory (ignored logs/caches are not listed).
# DO NOT merge this feature locally. You will merge it through a GitHub PR.

# ============================================================================
# 6. CREATE A PUBLIC GITHUB REPOSITORY YOURSELF, THEN PUSH
# ============================================================================
# BROWSER STEPS — perform these LIVE:
# 1. Sign in to GitHub and select New repository.
# 2. Enter the NEW, UNUSED repository name selected in Step 5; choose Public.
# 3. Leave README/.gitignore/license initialization empty: local files are ready.
# 4. Click Create repository and copy its HTTPS URL.
# 5. Replace the placeholder URL in the command below with that exact URL.
# Pause recording for any authentication. Do not show tokens/passwords.

# origin is a name for the remote; adding it does not upload code yet.
git remote add origin https://github.com/YOUR_GITHUB_USERNAME/YOUR_NEW_REPOSITORY.git
git remote -v
# Upload main, then the model branch retained as evidence, then the PR branch.
# -u records the upstream so Git knows which remote branch this branch tracks.
git push -u origin main
git push origin codex/oop-models
git push -u origin codex/course-service

# If authentication fails, complete your GitHub credential setup and retry.
# If origin already exists, STOP and inspect git remote -v; do not force-push.

# ============================================================================
# 7. CREATE, REVIEW, AND MERGE THE PULL REQUEST YOURSELF
# ============================================================================
# BROWSER STEPS:
# 1. Open Pull requests -> New pull request in YOUR new repository.
# 2. Select base: main (destination), compare: codex/course-service (feature).
# 3. Review Files changed: service, main, tests, README, workflow, and this guide.
# 4. Title: "Add course management service, tests, and documentation".
# 5. Description: explain enrollment behavior, try/except/logging, and the actual
#    local test outcome. Describe this as an in-memory educational application.
# 6. Click Create pull request. SHOW the PR URL, commits, and changed code.
# 7. Wait for both Python-version checks to pass. If a check fails, inspect it,
#    fix the feature locally, test, commit, and push this feature again.
# 8. Select Create a merge commit, then confirm the merge.
# 9. Keep the branch as evidence. Save the actual repository and PR URLs.
# SAY: "A Pull Request allows review before merging a feature into main."
# A solo demonstration is self-review; do not claim independent approval.

# ============================================================================
# 8. PULL THE GITHUB MERGE AND SHOW THE FINAL OUTPUT
# ============================================================================
git switch main
# Download and incorporate the GitHub merge without creating another local merge.
git pull --ff-only origin main
python main.py
python test_course_management.py
# Show the actual feature commits, local model merge, and GitHub PR merge.
git log --oneline --graph --all --decorate
git status --short --branch
# Expected: successful demo, 14 passing test groups, and a clean working directory.

# ============================================================================
# 9. FINISH RECORDING AND SUBMIT
# ============================================================================
# Explain the final output and that in-memory records reset when the program ends.
# Show your repository and PR URLs. Upload your recorded video to YouTube yourself.
# Submit the three actual URLs: repository, Pull Request, and YouTube video.
# No submission file or other missing guide is needed to follow this handout.
# Reference: https://git-scm.com/docs/git-init (init does not clear existing history)
# Reference: https://git-scm.com/docs/git-merge
# Reference: https://docs.github.com/en/pull-requests
