# Test Strategy

## Gherkin Decision

Who outside the engineering team will read these scenarios and be capable of telling us one is wrong?

Answer: Nobody

Decision: Do not adopt Gherkin.

Justification:

The current TalkDesk project does not have a non-engineering stakeholder who will actively review executable specifications. Adding Gherkin would introduce feature files, step definitions, and additional maintenance overhead without providing collaboration benefits. The project's acceptance criteria are already documented and traceable to automated tests. For this project, plain automated tests provide simpler maintenance, easier debugging, and clearer traceability while avoiding the additional abstraction layer required by Gherkin.

How acceptance criteria remain legible:

Acceptance criteria are maintained in docs/acceptance-criteria.md and are mapped directly to automated tests. This provides a readable specification without requiring a separate feature-file layer.


## Test Layers

- Unit tests for core logic.
- Integration tests for APIs and database interaction.
- End-to-End tests for complete user journeys.
``
