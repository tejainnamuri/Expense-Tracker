# Smart Expense Tracker API

A small REST API for tracking personal expenses, built with Python and Flask.

## What I built

- CRUD-style endpoints to add, list, filter, and delete expenses.
- Server-side validation (title, amount > 0, category, date in `YYYY-MM-DD`) with
  clear 400 responses instead of silently accepting bad data.
- Totals endpoint that returns both the overall total and a per-category breakdown.
- Data lives in memory and is mirrored to a local `data.json` file after every
  write, so it survives a server restart but needs no database setup.
- **Bonus implemented:** keyword search over expense titles/categories
  (`GET /expenses/search?q=...`).

## Tech stack

- Python 3.10+
- Flask (web framework)
- pytest (test suite, using Flask's test client — no running server required)

## Project structure

```
expense-tracker/
  README.md
  AI_NOTES.md
  requirements.txt
  run.py              # entry point: starts the dev server
  src/
    app.py            # Flask app + routes
    models.py          # request validation
    storage.py          # in-memory store + JSON persistence
  tests/
    test_api.py         # full test suite
```

## Setup & installation

```bash
git clone <your-repo-url>
cd expense-tracker
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Running the server

```bash
python run.py
```

The server starts at `http://localhost:5000`. Expenses are persisted to
`data.json` in the project root; delete that file to reset to an empty state.

## Running the tests

```bash
pytest tests/ -v
```

Tests use Flask's in-memory test client, so they never touch `data.json`
and can be run repeatedly without side effects.

## API reference

| Method | Endpoint                       | Description                                              |
|--------|---------------------------------|------------------------------------------------------------|
| POST   | `/expenses`                    | Add an expense                                            |
| GET    | `/expenses`                    | List all expenses (optional `?category=Food`)              |
| GET    | `/expenses/<id>`                | Get a single expense by id                                |
| DELETE | `/expenses/<id>`                | Delete an expense                                         |
| GET    | `/expenses/summary`             | Total overall + breakdown by category (optional `?category=Food` for a single total) |
| GET    | `/expenses/search?q=...`        | Search expenses by title/category keyword (bonus)          |
| GET    | `/health`                      | Health check                                               |

### Example requests

Add an expense:
```bash
curl -X POST http://localhost:5000/expenses \
  -H "Content-Type: application/json" \
  -d '{"title": "Lunch", "amount": 12.50, "category": "Food", "date": "2026-01-15"}'
```

List expenses in a category:
```bash
curl "http://localhost:5000/expenses?category=Food"
```

Get totals:
```bash
curl http://localhost:5000/expenses/summary
curl "http://localhost:5000/expenses/summary?category=Food"
```

Delete an expense:
```bash
curl -X DELETE http://localhost:5000/expenses/<id>
```

## Design decisions

- **IDs are server-generated (UUIDs)**, not accepted from the client, to avoid
  collisions and keep the API idempotent-safe on retries.
- **Category matching is case-insensitive** (`Food` and `food` are treated the
  same) since users are unlikely to be consistent about casing.
- **Validation lives in its own module** (`models.py`) separate from the Flask
  routes, so the rules can be unit-tested independently of HTTP if needed.
- **Persistence is a thin JSON mirror**, not a full storage engine — good
  enough for the stated scope ("in memory or a local JSON file"), and keeps
  the code readable in the ~4 hour budget.
