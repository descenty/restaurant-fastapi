#!/bin/bash
alembic init # do i need this?
alembic upgrade head
uvicorn main:app --host 0.0.0.0 --port 8000
