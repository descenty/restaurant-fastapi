#!/bin/bash
celery -A background.celery worker --loglevel=info -P gevent
