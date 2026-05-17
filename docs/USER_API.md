# User endpoints

This document describes the user-related API endpoints in the `app.api.endpoints.user` router.

- `GET /api/users/` — List users (paginated). Query params: `page`, `size`.
- `GET /api/users/profile/{user_id}` — Get a single user by ID.
- `POST /api/users/register` — Create a new user. Body: `UserCreate`.
- `PUT /api/users/update` — Update user. Query param: `user_id`, body: `UserUpdate`.
- `POST /api/users/upload` — Bulk upload users via CSV file (multipart file upload).
- `GET /api/users/view-pdf` — Example endpoint that returns a generated PDF (binary response).
- `GET /api/users/view` — Example endpoint that returns rendered HTML.

Notes
- The PDF and HTML endpoints return non-JSON responses and do not use the standard response model.
- See the `app.services` implementations for business logic (e.g. `UserService`, `PDFService`).

Example: curl to download PDF

```bash
curl -o invoice.pdf "http://localhost:8000/api/users/view-pdf"
```
