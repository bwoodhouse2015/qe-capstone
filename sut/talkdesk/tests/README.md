# The supplied suite

This is **the suite the planted defect D-9 refers to** — the tests that ship with
TalkDesk, as if written by the team that built it.

It is not the conformance suite. The two do different jobs:

| | `conformance/` | `tests/` (here) |
|---|---|---|
| Tests | The contract, over HTTP, against any implementation | The Python implementation, in-process |
| Asks | *Does this build match the contract, and are the defects still present?* | *Do the features work?* |
| Run by | Whoever is maintaining TalkDesk | The learner, on Week 1, with coverage on |
| Honest? | Yes | **Deliberately incomplete** |

## Why it is incomplete

A learner's first coverage report should show a real gap, not a contrived one.
This suite is written the way most real suites are written: the happy paths are
covered, the obvious errors are covered, and one validation branch that somebody
meant to come back to is not covered at all.

That branch is the **score-range rejection in `PATCH /api/talks/{id}`** —
defect D-9. The suite does patch a valid score, so the validation line itself is
green; what is never sent is a score outside 1–10, so the line that rejects it
is red. Line coverage looks fine. The branch is unverified.

That shape is the Week 1 exercise: *find what your tests do not touch, and
decide whether it matters* — and notice that the percentage would not have told
you.

**Do not add a test that patches an out-of-range score.** The conformance suite
parses this file and asserts that no such test exists, because adding one
deletes a Week 1 exercise for every future cohort.

## Running it

The suite needs the database up, because TalkDesk talks to Postgres rather than
mocking it:

```bash
docker compose up -d db --wait

cd python
pip install -r requirements.txt -r ../tests/requirements-dev.txt
DB_URL=postgresql://talkdesk:talkdesk@localhost:5432/talkdesk \
  python3 -m pytest ../tests -q --cov=app --cov-branch --cov-report=term-missing
```

Add `--cov-branch` and read the *Missing* column. The uncovered line numbers in
`app.py` are the point; the percentage is not.
