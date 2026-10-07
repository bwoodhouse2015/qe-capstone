# Refactor Log

## Refactor 1

Principle: Single Responsibility Principle (SRP)

Violation:
Validation and request handling were mixed together.

Change:
Separated validation logic from request-processing logic.

Result:
Code became easier to read and test.

---

## Refactor 2

Principle: Dependency Inversion Principle (DIP)

Violation:
Application logic depended directly on implementation details.

Change:
Used abstractions instead of concrete implementations.

Result:
Improved testability and maintainability.