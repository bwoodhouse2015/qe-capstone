# TalkDesk Acceptance Criteria

## AC1 (F)
A user can view submitted talks.

## AC2 (F)
A user can submit a new talk.

## AC3 (F)
A submitted talk must contain a title.

## AC4 (F)
A submitted talk must contain a speaker name.

## AC5 (F)
A user can search for talks.

## AC6 (F)
A reviewer can log in with valid credentials.

## AC7 (NF)
The application shall respond to requests within 2 seconds.

## AC8 (NF)
The application shall remain available during concurrent requests.

# Given / When / Then Scenarios

## Scenario 1

Given a speaker is on the submission page

When valid talk information is submitted

Then the talk is stored successfully

## Scenario 2

Given submitted talks exist

When a user searches by title

Then matching talks are displayed

## Scenario 3

Given a reviewer login page is displayed

When valid reviewer credentials are entered

Then the reviewer is authenticated