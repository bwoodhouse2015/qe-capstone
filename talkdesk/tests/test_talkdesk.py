"""The suite that ships with TalkDesk.

Written the way a real team writes one under deadline: happy paths covered,
obvious errors covered, and one validation branch nobody got back to.

That gap is deliberate and it is defect **D-9**. A valid score is patched here,
so the validation line runs; a score outside 1-10 never is, so the line that
rejects one never runs. Line coverage looks respectable and the branch is
unverified — the Week 1 exercise is to notice that the percentage did not tell
them.

**Do not add a test that patches an out-of-range score.**
`conformance/test_contract.py` parses this file and fails if one appears.

    docker compose up -d db --wait
    cd python && DB_URL=postgresql://talkdesk:talkdesk@localhost:5432/talkdesk \\
      python3 -m pytest ../tests -q --cov=app --cov-branch --cov-report=term-missing
"""
import pytest
from fastapi.testclient import TestClient

import app as talkdesk


@pytest.fixture(scope="module")
def client():
    with TestClient(talkdesk.app) as c:
        yield c


# ─────────────────────────────────────────────────────────────── health
def test_health_reports_ok(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


# ─────────────────────────────────────────────────────────── list talks
def test_list_returns_talks_with_speakers(client):
    r = client.get("/api/talks")
    assert r.status_code == 200
    talks = r.json()
    assert len(talks) == 100, "the list endpoint pages at 100"
    first = talks[0]
    assert {"id", "title", "track", "status", "score", "speaker",
            "created_at"} <= set(first)
    assert set(first["speaker"]) == {"id", "name"}


def test_list_filters_by_track(client):
    r = client.get("/api/talks", params={"track": "testing"})
    assert r.status_code == 200
    assert all(t["track"] == "testing" for t in r.json())


def test_list_filters_by_status(client):
    r = client.get("/api/talks", params={"status": "accepted"})
    assert r.status_code == 200
    assert all(t["status"] == "accepted" for t in r.json())


# ────────────────────────────────────────────────────────────── search
def test_search_matches_a_substring(client):
    r = client.get("/api/talks/search", params={"q": "test"})
    assert r.status_code == 200
    for t in r.json():
        assert "test" in t["title"].lower()


def test_search_with_no_matches_returns_empty(client):
    r = client.get("/api/talks/search", params={"q": "zzzzzznotatalk"})
    assert r.status_code == 200
    assert r.json() == []


# ──────────────────────────────────────────────────────────── one talk
def test_get_one_talk_includes_the_abstract(client):
    r = client.get("/api/talks/1")
    assert r.status_code == 200
    body = r.json()
    assert body["id"] == 1
    assert "abstract" in body
    assert set(body["speaker"]) == {"id", "name", "email", "bio"}


def test_get_missing_talk_is_404(client):
    r = client.get("/api/talks/99999999")
    assert r.status_code == 404


# ────────────────────────────────────────────────────────────── create
def test_create_a_talk(client):
    r = client.post("/api/talks", json={
        "speaker_id": 1, "title": "A perfectly ordinary talk",
        "abstract": "About ordinary things.", "track": "testing"})
    assert r.status_code == 201
    body = r.json()
    assert body["title"] == "A perfectly ordinary talk"
    assert body["status"] == "submitted", "new talks start as submitted"


def test_create_rejects_an_unknown_track(client):
    r = client.post("/api/talks", json={
        "speaker_id": 1, "title": "Wrong track", "track": "gardening"})
    assert r.status_code == 400


def test_create_rejects_an_unknown_speaker(client):
    r = client.post("/api/talks", json={
        "speaker_id": 999999, "title": "Nobody's talk", "track": "testing"})
    assert r.status_code in (400, 404)


# ─────────────────────────────────────────────────────────────── patch
#
# The happy paths are covered, including scoring. What is not covered is the
# *rejection* branch — nothing here ever sends a score outside 1–10. That is
# D-9, and it is meant to stay that way. Note the shape of the gap: the
# validation line runs on every valid score, so line coverage looks respectable
# while the branch is unverified.
def test_patch_updates_status(client):
    created = client.post("/api/talks", json={
        "speaker_id": 2, "title": "To be accepted", "track": "delivery"}).json()
    r = client.patch(f"/api/talks/{created['id']}", json={"status": "accepted"})
    assert r.status_code == 200
    assert r.json()["status"] == "accepted"


def test_patch_records_a_score(client):
    created = client.post("/api/talks", json={
        "speaker_id": 3, "title": "To be scored", "track": "culture"}).json()
    r = client.patch(f"/api/talks/{created['id']}", json={"score": 8})
    assert r.status_code == 200
    assert r.json()["score"] == 8


def test_patch_rejects_an_unknown_status(client):
    r = client.patch("/api/talks/1", json={"status": "maybe"})
    assert r.status_code == 400


def test_patch_with_nothing_to_update_is_rejected(client):
    r = client.patch("/api/talks/1", json={})
    assert r.status_code == 400


# ───────────────────────────────────────────────────────────────── HTML
def test_home_page_renders(client):
    r = client.get("/")
    assert r.status_code == 200
    assert "text/html" in r.headers["content-type"]


def test_submit_page_renders(client):
    r = client.get("/submit")
    assert r.status_code == 200
    assert "<form" in r.text
