psql -h localhost -U postgres -d fastapi_db

CREATE EXTENSION IF NOT EXISTS vector;
alembic upgrade head

uv pip install torch --index-url https://download.pytorch.org/whl/cpu
uv pip install sentence-transformers
