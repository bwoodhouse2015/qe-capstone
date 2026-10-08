# Coverage Baseline

Date: October 7, 2026

Coverage:
Pending execution of supplied TalkDesk test suite.

Notes:
TalkDesk test suite located at tests/test_talkdesk.py.
Coverage generation requires execution environment alignment with supplied course package.


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




## passed test

Name     Stmts   Miss Branch BrPart  Cover   Missing
----------------------------------------------------
app.py     121     10     28      3    90%   21, 41-42, 117, 156, 169, 183-185, 257
----------------------------------------------------
TOTAL      121     10     28      3    90%
18 passed, 1 warning in 1.51s
