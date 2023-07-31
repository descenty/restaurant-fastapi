FROM python:3.10-slim as requirements-stage

WORKDIR /tmp
RUN pip install poetry==1.5.1
COPY pyproject.toml poetry.lock .
RUN poetry export --without dev --without-hashes -f requirements.txt -o requirements.txt

FROM python:3.10-slim

WORKDIR /app
COPY --from=requirements-stage /tmp/requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY . .
CMD ["/bin/sh", "./start.sh"]