## Run FastAPI Mock App in Docker

The FastAPI mock application can be started locally in Docker for development, validation, and automated testing.

### Prerequisites

* Docker Desktop installed and running
* Docker configured for Linux containers

---

### Build the Docker Image

Run from the `sut/FastAPIMockApp` directory:

```bash
docker build -t fastapi-mock-enterprise-app:local .
```

---

### Start the Container

```bash
docker run -d --name fastapi-mock-enterprise-app -p 8080:8080 fastapi-mock-enterprise-app:local
```

This publishes the FastAPI service on:

```text
http://127.0.0.1:8080
```

---

### Verify the Application is Running

#### Health Endpoint

```bash
curl http://127.0.0.1:8080/health
```

Expected result:

```json
{"status":"ok"}
```

#### Swagger UI

Open in browser:

```text
http://127.0.0.1:8080/docs
```

---

### Check Container Health Status

```bash
docker inspect --format='{{.State.Health.Status}}' fastapi-mock-enterprise-app
```

Expected result:

```text
healthy
```

---

### View Container Logs

```bash
docker logs fastapi-mock-enterprise-app
```

---

### Stop and Remove the Container

```bash
docker rm -f fastapi-mock-enterprise-app
```

---

### Run Automated Startup Validation

To verify image build, startup, host accessibility, and internal container `/health` checks:

```bash
python tools/validate_container_startup.py
```

Expected result:

```text
External health check passed: http://127.0.0.1:8080/health
Internal container /health check passed.
FCAPI validation passed.
```

---

### Run from Repository Root

If starting from the parent repository root:

```bash
docker build -t fastapi-mock-enterprise-app:local -f sut/FastAPIMockApp/Dockerfile sut/FastAPIMockApp
docker run -d --name fastapi-mock-enterprise-app -p 8080:8080 fastapi-mock-enterprise-app:local
curl http://127.0.0.1:8080/health
docker rm -f fastapi-mock-enterprise-app
```
