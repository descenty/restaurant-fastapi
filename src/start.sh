#!/bin/bash
alembic init
alembic upgrade head
uvicorn main:app --host 0.0.0.0 --port 8000