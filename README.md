Restaurant-FastAPI
==========
To run the project using docker-compose, run the following command:
```bash
docker compose up --build -d
```
To test the project, run the following command:
```bash
docker compose -f .\docker-compose.test.yml up --build --abort-on-container-exit
```