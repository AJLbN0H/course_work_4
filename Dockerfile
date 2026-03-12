# Используем официальный образ Python 3.12 (slim - облегченная версия)
FROM python:3.13-slim

# Настройки Python и Poetry
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VERSION=2.1.1 \
    POETRY_VIRTUALENVS_CREATE=false

# Рабочая директория внутри контейнера
WORKDIR /app

# Устанавливаем системные зависимости для сборки psycopg2 (Postgres)
RUN apt-get update \
    && apt-get install -y gcc libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем Poetry
RUN pip install "poetry==$POETRY_VERSION"

# Копируем файлы зависимостей
COPY pyproject.toml poetry.lock* ./

# Устанавливаем зависимости проекта
RUN poetry install --no-interaction --no-ansi

# Копируем весь оставшийся код проекта
COPY . .