## Server
* `uv run uvicorn app.main:app --reload` - run server

## Migrations
* `uv run alembic upgrade head` - run migrations
* `uv run alembic revision --autogenerate -m "Initial migration"` - create migration
