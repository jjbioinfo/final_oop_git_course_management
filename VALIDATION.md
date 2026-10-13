# Validation — 13 October 2026

## Local checks completed

Environment: project `.venv`, Python 3.13.5, macOS. No third-party runtime dependencies.

| Check | Expected | Observed |
|---|---|---|
| Original baseline tests | Seven groups pass | Seven passed before editing |
| Revised script-mode tests | 14 groups, zero failures | Passed |
| Revised package-mode tests | Same 14 groups, zero failures | Passed |
| Demo execution | Exit 0; two students, mentor, courses, enrollments, handled duplicate | Passed |
| README Python example | Asha / Python OOP / Completed | Exact three-line output matched |
| Standard-library import | `platform.system` exists | Passed after renaming the local module |
| Shell guide syntax | Valid Bash | `bash -n git_workflow.sh` passed |
| Diff whitespace | No errors | `git diff --check` passed |

The suite covers abstraction, inheritance, polymorphism, read-only properties,
instance independence, static email checking, class factories, string/integer IDs,
missing records, duplicate IDs/enrollments, capacity boundaries, invalid types and
nulls, unchanged state after expected failure, repeated completion, log creation,
simulated log-file permission failure, and expected/unexpected CLI error exits.

The log-file failure is injected with `unittest.mock`; it is a controlled local
failure check. The email validation is a conservative format policy, not a DNS,
mailbox-ownership, or complete email-standard validation.

GitHub Actions is configured for Python 3.10 and 3.13. Its live result will be
recorded after publication; local testing alone does not establish those CI results.

## Limitations

This checks a single-process, in-memory teaching program. Persistence, concurrent
transactions, user authentication/authorization, hosted operation, and real
production readiness are not implemented or certified. The recording script does
not fulfill the YouTube submission until the learner records and uploads a video.
