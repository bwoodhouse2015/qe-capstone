Functional Acceptance Criteria (6)

F1 – Search Talks
Given talks containing a search keyword exist,
 When a user searches for that keyword,
 Then matching talks are returned in the search results.
Coverage:
Unit: TBD
Integration: test_search_matches_a_substring
E2E: test_search_talk.py

F2 – Empty Search Results
Given no talks contain the search keyword,
When a user performs a search,
Then an empty result set is returned.
Coverage:
Unit: TBD
Integration: test_search_with_no_matches_returns_empty
E2E: test_search_talk.py

F3 - Submit Talk
Given a valid speaker exists in the system,
When a user submits a talk with valid title, abstract, and track information,
Then the talk is created successfully and assigned a unique identifier.
Coverage:
Unit: TBD
Integration: test_create_a_talk
E2E: test_submit_talk.py

F4 - Reject Invalid Speaker
Given a speaker ID does not exist,
When a user submits a talk using that speaker ID,
Then the request is rejected and an error response is returned.
Coverage:
Unit: TBD
Integration: test_create_rejects_an_unknown_speaker
E2E: TBD

F5 - Update Talk Status
Given an existing talk exists,
When an authorized user updates the talk status,
Then the new status is stored and returned in subsequent requests.
Coverage:
Unit: TBD
Integration: test_patch_updates_status
Integration: test_patch_rejects_an_unknown_status
E2E: TBD

F6 – Retrieve Talk Details
Given an existing talk exists,
 When a user requests the talk details,
 Then the talk information and associated speaker information are returned.
Coverage:
Unit: TBD
Integration: test_get_one_talk_includes_the_abstract
Integration: test_get_missing_talk_is_404
E2E: TBD



Non-Functional Acceptance Criteria (4)

NF7 - Search Performance
Given a database containing 50,000 talks,
When a search request is executed,
Then results are returned within 2 seconds under normal operating conditions.
Coverage:
Unit: N/A
Integration: TBD
Performance: Week 3
E2E: N/A

NF8 - Security
Given an unauthenticated request,
When access to a protected operation is attempted,
Then access is denied and no sensitive application or database information is exposed.
Coverage:
Unit: TBD
Integration: TBD
Security: Week 3
E2E: TBD

NF9 - Reliability 
Given valid talk data is submitted,
When the submission request succeeds,
Then the talk data remains available after application restart.
Coverage:
Unit: N/A
Integration: TBD
Reliability: Week 3
E2E: TBD

N10 - Data Integrity
Given a talk is created,
When the talk is retrieved through the API,
Then the stored values match the values originally submitted.
Coverage:
Unit: TBD
Integration: test_create_a_talk
Integration: test_talks_api_response_contract
E2E: test_submit_talk.py
