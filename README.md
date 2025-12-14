## Server
* `uv run uvicorn app.main:app --reload` - run server

## Migrations
* `uv run alembic upgrade head` - run migrations
* `uv run alembic revision --autogenerate -m "Initial migration"` - create migration

## Development
- **Start**: `./scripts/start.sh` (Starts Redis, Worker, Server, and SAQ Web)
- **Stop**: `./scripts/stop.sh`

## Access
- **API Docs**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **SAQ Web**: [http://127.0.0.1:8081](http://127.0.0.1:8081)
