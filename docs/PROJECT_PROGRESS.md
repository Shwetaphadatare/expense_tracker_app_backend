# Expense Tracker Backend Progress

## Sprint 1 — Backend Foundation
- FastAPI project structure
- Environment config
- PostgreSQL connection
- Health check API

## Sprint 2 — User Security Foundation
- SQLAlchemy Base
- User model
- Pydantic schemas
- Password hashing

## Sprint 3 — User Registration
- /auth/register
- Duplicate email validation
- Password hashing before DB save

## Sprint 4 — JWT Login Authentication
- /auth/login endpoint implemented
- Password verification added
- JWT token generation configured
- Access token expiry added
- Secure secret key integration completed

## Sprint 5 — Protected User Authorization
- JWT token verification implemented
- Current authenticated user dependency created
- /users/me protected endpoint added
- Token expiration and invalid token handling completed

## Sprint 6 — Expense CRUD Core
- Expense model created
- Expense schema validation added
- Protected expense creation endpoint implemented
- User-specific expense listing added
- Expense ownership security enforced

## Sprint 7 — Expense Update and Delete
- Expense update endpoint implemented
- Expense delete endpoint implemented
- Ownership validation enforced for modifications
- Secure expense-by-ID filtering added
- Unauthorized cross-user access prevented

## Sprint 8 — Expense Filtering and Pagination
- Category filtering implemented
- Date range filtering added
- Pagination with skip/limit added
- Sorting by creation date supported
- Query performance and scalability improved