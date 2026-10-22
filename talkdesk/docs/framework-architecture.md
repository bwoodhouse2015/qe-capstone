# TalkDesk Test Framework Architecture

## Base Layer
Shared fixtures, browser setup, API clients, and reusable initialization code.

## Pages Layer
Page Objects representing TalkDesk pages and user actions.

## Utilities Layer
Reusable helpers, assertions, reporting, and test data generation.

## Configuration Layer
Environment settings, URLs, credentials, and timeouts.

## Test Layers

### Unit Tests
Validate isolated logic and business rules.

### Integration Tests
Validate API and database interactions.

### End-to-End Tests
Validate complete user journeys.





# Framework Architecture

## Page Object Pattern

Layer:
pages/

Symptom:
A UI change could require updates in many tests.

Cost:
Additional abstraction layer and another file to maintain.

Expected cheaper change:
If the login page selectors change, only LoginPage must be updated instead of every login-related test.

---

## Factory Pattern

Layer:
base/

Symptom:
Browser creation logic can become duplicated across tests.

Cost:
Additional indirection between tests and browser initialization.

Expected cheaper change:
Adding Firefox support requires updating one factory instead of modifying every test file.
