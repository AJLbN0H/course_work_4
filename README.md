# MailFlow Automation Service

Django application for planning and running **email campaigns** (newsletters): recipients, message templates, send windows, and delivery attempts. Background work uses **Celery** with **Redis** as broker/cache; **Celery Beat** can trigger periodic tasks (e.g. sending active newsletters).

![Python](https://img.shields.io/badge/python-3.13+-blue.svg)
![Django](https://img.shields.io/badge/django-5.2+-green.svg)
![Celery](https://img.shields.io/badge/celery--beat-enabled-orange.svg)
![Redis](https://img.shields.io/badge/redis-broker-red.svg)
[![Tests](https://github.com/AJLbN0H/mailflow-automation-service/actions/workflows/tests.yml/badge.svg)](https://github.com/AJLbN0H/mailflow-automation-service/actions/workflows/tests.yml)

## Features

- **Recipients (CRM-style)** — store mailing recipients with owner-scoped access where applicable.
- **Messages** — reusable email subjects and bodies linked to campaigns.
- **Newsletters** — schedule send start/end, attach recipients, track status; optional disable flag.
- **Send attempts** — logging of send outcomes for troubleshooting.
- **Auth** — Django session auth; custom user model in `users`.
- **SMTP** — Yandex SMTP settings via environment variables (`EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`).
- **Caching & tasks** — Redis-backed cache in production-like runs; Celery worker + beat for async and scheduled jobs.

## Stack

| Layer        | Technology                          |
| ------------ | ----------------------------------- |
| Web UI       | Django (MTV), templates + Bootstrap |
| DB           | PostgreSQL                          |
| Tasks        | Celery                              |
| Scheduler    | Celery Beat                         |
| Broker/cache | Redis                               |
| Deps / tests | Poetry, pytest, pytest-django       |

## Project layout

- `mailings/` — models, views, forms, tasks, templates, management commands for mailings.
- `users/` — custom `User` model, registration, login, profile/update views.
- `config/` — Django settings, URLs, WSGI/ASGI, Celery app.
- `tests/` — pytest suite (`pytest.ini` sets `DJANGO_SETTINGS_MODULE=config.settings`).
- `static/` — static assets.

## Quick start (Docker)

1. Clone the repo:

   ```bash
   git clone https://github.com/AJLbN0H/mailflow-automation-service.git
   cd mailflow-automation-service
   ```

2. Copy the environment template and adjust values:

   ```bash
   cp .env.sample .env
   ```

   Set at least `SECRET_KEY`, database fields (`NAME`, `USER`, `PASSWORD`, `HOST`, `PORT` — use `HOST=db` inside Compose), `CACHE_LOCATION` (e.g. `redis://redis:6379/1`), and SMTP credentials for real sends.

3. Start the stack:

   ```bash
   docker compose up --build
   ```

   The `web` service runs migrations then `runserver`. By default the app is published on **http://localhost:8001** (`WEB_PORT` defaults to `8001` to avoid clashes with a local service on `8000`). Override with `WEB_PORT` in `.env` if needed.

4. Run tests inside Docker (one-off container using the `web` image):

   ```bash
   docker compose run --rm web poetry run pytest
   ```

> **Secrets:** do not commit real keys. Use `.env` (ignored by git) or your host/CI secret store. Compose interpolates variables from the shell and from a root `.env` file.

## Local run (without Docker)

You need **PostgreSQL** and **Redis** running locally. In `.env`, set `HOST=127.0.0.1` (or your host), matching `NAME` / `USER` / `PASSWORD` / `PORT`, and point `CACHE_LOCATION` at your Redis (e.g. `redis://127.0.0.1:6379/1`).

```bash
poetry install
cp .env.sample .env   # then edit for local DB/Redis/SMTP

poetry run python manage.py migrate
poetry run python manage.py runserver
```

### Tests (local)

`pytest` is configured so the suite uses an isolated **SQLite** DB and in-memory Celery/cache backends (no Postgres/Redis required for `pytest`):

```bash
poetry run pytest
```

## Celery (local)

```bash
celery -A config worker -l info
celery -A config beat -l info
```

Use the same `.env` as the web app so `CACHE_LOCATION` / broker URLs match Redis.

## CI

GitHub Actions runs on pushes/PRs to `main` / `develop` (PRs target `main`): **Python 3.13**, service containers **PostgreSQL 15** and **Redis 7**, then `poetry install` and **`poetry run pytest`**.

Workflow file: [`.github/workflows/tests.yml`](.github/workflows/tests.yml).

> The project is managed with **Poetry** (`pyproject.toml` + `poetry.lock`). There is no `requirements.txt`; CI installs dependencies via Poetry.

## Roadmap

- Broader integration tests and coverage.
- Optional OpenAPI or admin-focused docs.
- Stronger production hardening (secrets manager, HTTPS, non-dev server).
