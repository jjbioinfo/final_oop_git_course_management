#!/usr/bin/env bash
# Run from this assignment's own repository. This file only inspects existing work.
# Do not re-initialize or replay old commits when recording the video.
set -euo pipefail

git status --short --branch
git branch --all
git log --oneline --graph --all --decorate

# Show the actual local feature merge and the Pull Request merge in the graph.
# Online inspection, after gh auth login:
# gh repo view --web
# gh pr list --state all
# gh pr view PR_NUMBER
# gh pr diff PR_NUMBER

# Example future development cycle (copy one command at a time; not run here):
# git switch main
# git pull --ff-only
# git switch -c codex/your-feature
# ... edit the relevant source and tests ...
# python test_course_management.py
# git diff --check
# git add path/to/changed_file.py path/to/changed_test.py
# git commit -m "Describe the specific change and its purpose"
# git push -u origin codex/your-feature
# gh pr create --base main --head codex/your-feature --title "Your feature" --body-file pr-body.md
# ... review the diff and wait for automated checks ...
# gh pr merge PR_NUMBER --merge
# git switch main
# git pull --ff-only
