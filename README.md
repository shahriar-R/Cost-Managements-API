# Expense Management API (FastAPI + Docker + Redis + PostgreSQL)

This project is a **FastAPI-based Expense Management System** that provides:
- **JWT Authentication** (Access & Refresh Tokens with HttpOnly cookies)
- **CRUD operations** for managing expenses
- **Database integration** using PostgreSQL and SQLAlchemy (async)
- **Caching layer** with Redis
- **Structured error handling** with custom exceptions
- **Tests** using `pytest` and `locust` (load testing)
- **Docker & Docker Compose** setup for containerized deployment

---

## 🚀 Features
- Authentication with JWT (secure HttpOnly cookies)
- Expense CRUD (Create, Read, Update, Delete)
- Redis integration for caching and session management
- Database migrations via Alembic
- Unit & integration tests
- Load tests with Locust

---
## 🛠️ Multi-Stage Builds in Docker

**A multi-stage build means creating a Docker image in multiple steps (stages), where each stage has its own base image and purpose.**
Why use Multi-Stage builds?

- Smaller images → you copy only the necessary artifacts to the final image
- Security → dev tools and unnecessary files are excluded from production
- Better caching → dependencies and source code are separated
- Faster builds → no need to rebuild everything if only part of the code changes

```bash
# Stage 1: Build dependencies
FROM python:3.12-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user -r requirements.txt

# Stage 2: Production image
FROM python:3.12-slim
WORKDIR /app

# Copy dependencies from builder
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

# Copy app source code
COPY ./app /app

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```
### 🔹 How it works?
- The builder stage installs all dependencies.
- The production stage copies only the installed packages + source code.
- The final image is much smaller and only includes what’s required to run the API.

## 🐳 Running with Docker Compose
```bash
  docker-compose up --build
```
## 🧪 Running Tests
### Unit & Integration Tests
```bash
pytest -v
```
## Load Tests with Locust
```bash
locust -f core/locustfile.py
```
