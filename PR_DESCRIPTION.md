# Fix: tests, health endpoint, JWT init

Short summary
-------------

Initialize `JWTManager`, add a `/health` endpoint, align API responses/status codes with tests, add password strength validation, and remove a tracked `node_modules` artifact that exceeded GitHub's file-size limit.

Changes
-------

- `planventure-api/app.py`: JWT initialization, enable CORS, add `/health` endpoint (returns `{"status": "healthy"}`), support login by email or username, validate password strength on registration, and adjust create/update/delete responses and status codes to match tests.
- `planventure-api/test_flask.py`: renamed route handler to avoid pytest collecting it as a test.
- Removed `planventure-api/test_results.txt` which caused pytest collection/encoding issues.
- Cleaned large tracked files by removing `planventure-web/node_modules` from the branch commit (was >100MB and blocked push).

Tests
-----

All tests pass locally in the repository virtualenv:

```
27 passed, 3 warnings
```

Notes
-----

- SQLAlchemy `Query.get()` is deprecated — consider migrating to `Session.get()` in a follow-up.
- The branch removed large node_module files from tracking; consider adding `planventure-web/node_modules` to `.gitignore` if not already present.

Suggested reviewers/labels
--------------------------

- Reviewers: @backend, @qa
- Labels: `backend`, `tests`, `bugfix`

Compare/PR URL
--------------

https://github.com/itech4real/planventure/compare/main...fix/tests-and-health
