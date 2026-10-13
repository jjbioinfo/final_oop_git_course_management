#!/usr/bin/env bash

# Complete Git and GitHub workflow for the final mini project.
# This script is intentionally not executed during project creation.
# Review it, authenticate GitHub CLI, and run it while recording the video.

set -e

REPOSITORY_NAME="course-management-system"

echo "Step 1: Confirm GitHub authentication"
gh auth status

echo "Step 2: Initialize the repository"
git init -b main
git config user.name >/dev/null
git config user.email >/dev/null
git status

echo "Step 3: Create the initial project-setup commit"
git add \
    .gitignore \
    README.md \
    VIDEO_SCRIPT.md \
    exceptions.py \
    git_workflow.sh \
    logging_config.py \
    validators.py
git status
git commit -m "Set up Course Management System project"

echo "Step 4: Build the user models on a feature branch"
git checkout -b feature/user-models
git add user.py
git commit -m "Add abstract User, Student, and Mentor models"
git log --oneline --decorate -5

echo "Step 5: Merge the user feature branch locally"
git checkout main
git merge --no-ff feature/user-models -m "Merge user models feature"

echo "Step 6: Build course management on a second feature branch"
git checkout -b feature/course-management
git add course.py enrollment.py
git commit -m "Add Course and Enrollment models"

git add platform.py
git commit -m "Add course-management service layer"

git add main.py __init__.py
git commit -m "Add complete application demonstration"

git add test_course_management.py
git commit -m "Add Course Management System tests"

echo "Step 7: Demonstrate differences and inspect history"
git diff main...feature/course-management
git log --oneline --graph --all --decorate
git status

echo "Step 8: Run the application tests before publishing"
python test_course_management.py

echo "Step 9: Create an empty public GitHub repository"
gh repo create "$REPOSITORY_NAME" \
    --public \
    --source=. \
    --remote=origin

echo "Step 10: Push main and the Pull Request branch"
git push -u origin main
git push -u origin feature/course-management
git remote -v

echo "Step 11: Create the Pull Request"
PR_URL=$(gh pr create \
    --base main \
    --head feature/course-management \
    --title "Add complete course management functionality" \
    --body "Implements Course, Enrollment, service-layer coordination, the application demonstration, and automated tests.")
echo "Pull Request: $PR_URL"

echo "Step 12: Inspect and merge the Pull Request"
gh pr view "$PR_URL"
gh pr merge "$PR_URL" --merge --delete-branch

echo "Step 13: Update the local main branch"
git checkout main
git pull --ff-only origin main

echo "Step 14: Save repository and Pull Request URLs"
REPOSITORY_URL=$(gh repo view --json url --jq .url)
printf '# Submission Links\n\n- Repository: %s\n- Pull Request: %s\n' \
    "$REPOSITORY_URL" "$PR_URL" > SUBMISSION_LINKS.md
git add SUBMISSION_LINKS.md
git commit -m "Add submission links"
git push origin main

echo "Step 15: Display final status and history"
git status
git log --oneline --graph --all --decorate
echo "Repository: $REPOSITORY_URL"
echo "Pull Request: $PR_URL"
