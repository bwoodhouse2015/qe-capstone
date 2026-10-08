# Coverage Baseline

**Date:** October 7, 2026

## Initial Test Run

- Tests passed: 17
- Tests failed: 1
- Total tests: 18
- Line and branch coverage: 90%
- Failing test: `test_submit_page_renders`
- Failure reason: `/submit` returned `Handler.` instead of an HTML form.

## Command Used

`python -m pytest /app/tests -q --cov=app --cov-branch --cov-report=term-missing`