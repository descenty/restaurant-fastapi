#!/bin/bash
celery -A background.celery beat
