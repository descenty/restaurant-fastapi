FROM python:3.11-slim-bookworm as requirements-stage

WORKDIR /tmp
RUN pip install poetry==1.5.1
COPY src/pyproject.toml src/poetry.lock .
RUN poetry export --without dev --without-hashes -f requirements.txt -o requirements.txt

FROM python:3.11-slim-bookworm

WORKDIR /app
COPY --from=requirements-stage /tmp/requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY src .en[v] .
RUN chmod 755 ./start.sh
CMD ["./start.sh"]