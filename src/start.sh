#!/bin/bash
while !</dev/tcp/postgres/5432; do sleep 1; done;
alembic upgrade head
uvicorn main:app --host 0.0.0.0 --port 8000