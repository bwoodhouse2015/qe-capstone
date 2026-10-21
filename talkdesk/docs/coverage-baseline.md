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


**Date  October 18, 2026

Observation:
22 tests passed.

Runtime:
43m 20s

Potential causes:
- 50,000 row seed dataset
- N+1 query pattern in /api/talks
- Real database integration tests
- Python 3.14 environment
