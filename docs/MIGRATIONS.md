# Schema migrations

NextGenERP uses **Alembic** for versioned schema migrations. The baseline
revision (`0001`, "baseline current schema") creates the complete current
schema, including the Phase 2 security tables and integrity constraints.

The legacy `database/migrations.py::ensure_schema()` helper is retained for
compatibility and is invoked by the application at startup. It is no longer the
authoritative source of schema changes.

## Current head

- `0001` — baseline current schema.

## Running migrations

Run these commands from `backend/`:

```powershell
# Fresh or versioned database
python -m alembic upgrade head

# Existing unversioned database (preserves data)
python migrate.py

# Rehearse a rollback on a disposable database
python -m alembic downgrade base
```

`migrate.py` detects an unversioned application database, applies the
additive `create_all`/`ensure_schema` updates, and stamps the baseline at head.
It does **not** modify or delete application data.

## Backup and rollback procedure

1. Take a restorable backup before upgrading any real database.
2. Run `python migrate.py` or `python -m alembic upgrade head`.
3. Verify `/health`, the audit-log read endpoint, and a sample product/order
   query.
4. If rollback is required, restore the backup rather than relying on
   `alembic downgrade base`: the baseline downgrade drops all tables and is
   intended only for disposable databases.

## PostgreSQL verification

PostgreSQL is not available in this development environment (no `docker` or
`psql` binary). The following commands document the intended verification:

```powershell
docker compose up -d db
$env:DATABASE_URL = "postgresql+psycopg://user:pass@127.0.0.1:5432/nextgenerp"
python migrate.py
$env:TEST_POSTGRES_URL = "postgresql+psycopg://user:pass@127.0.0.1:5432/nextgenerp_test"
python -m pytest tests/test_postgres_parity.py -q
```

The parity suite is automatically skipped unless `TEST_POSTGRES_URL` points at
a disposable database whose name contains `test`.

## SQLite limitations

- SQLite cannot add a `CHECK` constraint to an existing table without
  rebuilding it. Model-level constraints therefore apply to fresh SQLite
  databases, while existing databases receive equivalent `BEFORE INSERT` and
  `BEFORE UPDATE` triggers from `ensure_schema()`.
- SQLite stores `TIMESTAMP WITH TIME ZONE` values without offset; the backend
  treats them as UTC. This is documented as a known limitation.
- `with_for_update()` is a no-op on SQLite; row locking is exercised only on
  PostgreSQL.
