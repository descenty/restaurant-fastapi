#!/bin/bash
sleep 5
alembic init
alembic upgrade head
uvicorn main:app --host 0.0.0.0 --port 8000