# Team Finder

Бэкенд веб-приложения **Team Finder** — платформа для поиска команды для совместных проектов. Пользователи могут создавать проекты, искать сотрудников и записываться на участие в проектах других.

## Стек

- Python 3.12+
- Django 5.2
- PostgreSQL 16
- Docker / Docker Compose

## Запуск через Docker

1. Скопируйте `.env_example` в `.env` и заполните переменные:

```bash
cp .env_example .env
```

2. Запустите приложение:

```bash
docker compose up -d --build
```

3. Выполните миграции и соберите статические файлы:

```bash
docker compose exec backend python manage.py migrate
docker compose exec backend python manage.py collectstatic --no-input
```

4. Приложение доступно по адресу: http://localhost

## Запуск без Docker (локальная разработка)

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Структура проекта

```
team_finder/      # главный Django-проект
├── projects/         # приложение: проекты (models, views, forms, urls)
├── users/            # приложение: пользователи (models, views, forms, urls)
├── templates_var1/   # HTML-шаблоны (вариант 1 — Избранное)
├── static/           # CSS, JS, изображения
├── docker-compose.yml
├── requirements.txt
└── .env_example
```

## Особенности реализации

- Используется вариант **1** (шаблоны `templates_var1/`): избранные проекты (сердечко), фильтрация пользователей по 4 критериям.
- `toggle_favorite` — эндпоинт `POST /projects/toggle-favorite/` (без pk в URL, pk передаётся в теле запроса как `project_id`).
- Аватарка пользователя генерируется автоматически при регистрации (первая буква имени на цветном фоне).

## Переменные окружения (.env)

```
DJANGO_SECRET_KEY=your-secret-key
DJANGO_DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
POSTGRES_DB=team_finder
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=db
POSTGRES_PORT=5432
```
