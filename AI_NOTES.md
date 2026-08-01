# AI Notes

**Tool used:** Claude (Anthropic), via the claude.ai chat interface.

## 1. What was AI-generated vs. written by me

**[TODO — personalize before submitting]** This first draft was scaffolded
end-to-end by Claude in one pass: `src/app.py`, `src/models.py`,
`src/storage.py`, `run.py`, `tests/test_api.py`, and the README. Replace this
paragraph with what's actually true for you by the time you submit — which
files you left as-is, which you edited, and anything you wrote yourself (an
extra test, a route you changed, a validation rule you tightened, an error
message you reworded, etc.). "AI wrote everything, unchanged" is a valid
answer only if it's true — and it's exactly the kind of generic answer this
section is meant to screen for, so reviewers will be looking for specifics.

## 2. What I validated, tested, or changed, and why

I ran the generated test suite (`pytest tests/ -v`) and confirmed all 19
tests pass. I also started the server with `python run.py` and manually
exercised every endpoint with `curl` — add, list, filter by category,
summary (overall and per-category), and delete — to confirm the JSON shapes
and status codes match what the README documents, and confirmed `data.json`
is written after each change and reloaded correctly on restart.

**[TODO — add your own findings]** Things worth actually poking at before you
call this done:
- Does `/expenses/summary?category=Foo` behave sensibly for a category with
  zero expenses (currently returns `{"category": "Foo", "total": 0}`)?
- What should happen if `amount` is sent as a string like `"12.50"`? Right
  now it's coerced to a float — is that the behavior you want?
- Deleting an already-deleted expense currently returns `404` on the second
  call. Would you rather it be idempotent (`204` both times)?
- Is a UUID the right id strategy for this scope, or would a short
  incrementing integer be easier to work with in a quick demo?

Document what you actually tried, what you found, and anything you changed
as a result — that's the part reviewers can't get from reading the diff
alone.

## 3. AI suggestions I didn't use, and why

A couple of directions were considered and deliberately not taken:

- **OpenAPI/Swagger docs as the bonus feature** — would have pulled in an
  extra dependency (e.g. `flasgger`) and generated schema for a fairly small
  API surface. Keyword search was picked instead since the assignment caps
  the bonus at one feature, and search shows the same "read the spec, pick a
  proportionate scope" judgment without the added moving parts.
- **A SQLite/ORM storage layer** — the assignment explicitly allows in-memory
  or a local JSON file, so a database would be over-engineering relative to
  the stated scope and the ~4 hour budget.

**[TODO — add your own]** Note anything *you* rejected, simplified, or
overrode from what the AI suggested while you were reviewing this.
