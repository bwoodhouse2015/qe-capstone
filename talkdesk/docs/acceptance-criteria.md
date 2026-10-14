Functional Acceptance Criteria (6)


AC1 – Agent Login
Given a registered agent with valid credentials,
When the agent signs in,
Then the agent is successfully authenticated and redirected to the TalkDesk dashboard.

AC2 – Invalid Login Handling
Given an agent enters invalid credentials,
When the login request is submitted,
Then access is denied and an appropriate error message is displayed.

AC3 – Contact Search
Given customer records exist in the system,
When an agent searches using a valid customer identifier,
Then matching customer information is returned.

AC4 – Call Creation
Given an authenticated agent,
When the agent initiates an outbound call,
Then the call is created and displayed in the active call list.

AC5 – Call Status Updates
Given an active call exists,
When the call state changes (ringing, connected, ended),
Then the updated status is reflected in the interface.

AC6 – Call History Retrieval
Given completed calls exist,
When an agent views call history,
Then previous call records are displayed with relevant details.




Non-Functional Acceptance Criteria (2)

AC7 – Performance
The system shall return dashboard and call-related requests within 2 seconds for normal operating conditions.

AC8 – Security
The system shall prevent unauthorized access to agent and customer data and require authentication for protected functions.