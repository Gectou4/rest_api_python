# G4Api - Mini API REST (Python)

Lightweight REST API in Python with Flask and MySQL. No heavy framework, JSON output by default (Markdown via `Accept: text/markdown` header).

[![CI](https://github.com/Gectou4/rest_api_python/actions/workflows/ci.yml/badge.svg)](https://github.com/Gectou4/rest_api_python/actions/workflows/ci.yml)

> **Part of the G4Api series.** The same small API (users, tasks and their N:N link) built in several stacks, to compare ecosystems: language, tooling, tests, static analysis and CI. Learning project. The PHP version is the reference: written by hand, then polished with AI-assisted review. The other stacks were ported from it in May 2026 with the help of an AI coding assistant.
>
> | Stack                | Repository                                                                |
> | -------------------- | ------------------------------------------------------------------------- |
> | PHP 8 (no framework) | [rest_api_php](https://github.com/Gectou4/rest_api_php)                   |
> | Go                   | [rest_api_go](https://github.com/Gectou4/rest_api_go)                     |
> | Rust (axum, sqlx)    | [rest_api_rs](https://github.com/Gectou4/rest_api_rs)                     |
> | Java 21 (Jersey)     | [rest_api_java](https://github.com/Gectou4/rest_api_java)                 |
> | .NET 8 (Dapper)      | [rest_api_netcsharp](https://github.com/Gectou4/rest_api_netcsharp)       |
> | Python (Flask)       | [rest_api_python](https://github.com/Gectou4/rest_api_python) (this repo) |
> | Node.js (Express)    | [rest_api_nodejs](https://github.com/Gectou4/rest_api_nodejs)             |
> | React front-end      | [rest_api_front_react](https://github.com/Gectou4/rest_api_front_react)   |

## Objects

- **User** - managed via API
- **Task** - managed via API with status tracking

### Task Status

| Value | Status |
|-------|--------|
| 1 | Backlog |
| 2 | Todo |
| 3 | In Progress |
| 4 | Done |
| 5 | Closed |

## Endpoints

| Method | URI | Description |
|--------|-----|-------------|
| `GET` | `/user/{id}` | Get user by ID |
| `GET` | `/user/{id}/task` | Get all tasks for a user |
| `POST` | `/task` | Create a new task |
| `PUT` | `/task` | Create a new task (alias) |
| `POST` | `/task/{id}` | Update an existing task |
| `PUT` | `/task/{id}` | Update an existing task (alias) |
| `DELETE` | `/task/{id}` | Delete a task |
| `POST` | `/user/{userId}/task/{taskId}` | Associate task to user |
| `PUT` | `/user/{userId}/task/{taskId}` | Associate task to user (alias) |
| `DELETE` | `/user/{userId}/task/{taskId}` | Remove task from user |

## Prerequisites

- Python 3.12+
- MySQL 8.0+ / MariaDB 10.4+
- Docker & Docker Compose (optional, recommended)

## Installation

### With Docker (recommended)

```bash
docker compose up -d
```

API available at `http://localhost:5000`

### Without Docker

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set environment variables:
```bash
export DB_USER=root
export DB_PWD=
export DB_HOST=localhost
export DB_NAME=rest_api
```

3. Initialize the database:
```bash
mysql -u root -p rest_api < share/sql/rest_api.sql
```

4. Run the API:
```bash
python -m flask run --host=0.0.0.0 --port=5000
```

## Configuration

Database connection is configured via environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `DB_USER` | `root` | Database username |
| `DB_PWD` | `` | Database password |
| `DB_HOST` | `localhost` | Database host |
| `DB_PORT` | `3306` | Database port |
| `DB_NAME` | `rest_api` | Database name |

## Code Quality

### Lint

```bash
ruff check src/ tests/
```

### Format

```bash
ruff format src/ tests/
```

## Tests

### With Docker

```bash
docker compose run --rm test
```

### Without Docker

```bash
pytest tests/ -v
```

Tests require a running MySQL database with the schema initialized.

## Response Format

- **Default**: `application/json` (pretty-printed)
- **Alternative**: `text/markdown` (send `Accept: text/markdown` header)

CORS headers are set on all responses.

## Adding a Controller

1. Create a new file in `src/controllers/`
2. Inherit from `BaseController`
3. Add route pattern in `src/app.py` ROUTES list
4. Implement action methods

## Project Structure

```
rest_api_python/
├── src/
│   ├── app.py                 # Flask app + routes
│   ├── config/
│   │   └── db.py              # Database configuration
│   ├── models/
│   │   ├── base.py            # BaseModel + DB singleton
│   │   ├── user.py            # User model
│   │   ├── task.py            # Task model
│   │   ├── task_status.py     # TaskStatus enum
│   │   └── user_task.py       # User-Task relationship
│   └── controllers/
│       ├── base.py            # BaseController
│       ├── user.py            # User endpoints
│       └── task.py            # Task endpoints
├── tests/
│   ├── conftest.py            # Pytest fixtures
│   └── test_api.py            # API integration tests
├── share/sql/
│   └── rest_api.sql           # Database schema + seed
├── docker/
│   ├── Dockerfile             # API image
│   └── Dockerfile.test        # Test image
├── docker-compose.yml         # API + MySQL + Test
├── .github/workflows/
│   └── ci.yml                 # CI/CD pipeline
├── pyproject.toml             # Project config (ruff, pytest)
├── requirements.txt           # Python dependencies
└── README.md
```
