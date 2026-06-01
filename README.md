# Team Finder

Бэкенд веб-приложения **Team Finder** — платформа для поиска команды для совместных проектов. Пользователи могут создавать проекты, искать сотрудников и записываться на участие в проектах других.

## Стек

*   Python 3.12+
*   Django 5.2
*   PostgreSQL 16
*   Docker / Docker Compose

## Запуск через Docker

1. Скопируйте `.env_example` в `.env` и заполните переменные:

```bash
cp .env_example .env
```

2. Запустите приложение:

```bash
docker compose up -d --build
```

3. Приложение доступно по адресу: [http://localhost:8000](http://localhost:8000)

Docker Compose автоматически выполняет:
*   Миграции БД
*   Сбор статических файлов
*   Создание тестовых данных (пользователи и проекты)

## Запуск без Docker (локальная разработка)

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py create_test_data
python manage.py runserver
```

## Тестовые данные

При запуске через Docker Compose создаются тестовые пользователи:

| Email                | Пароль      | Имя              |
|----------------------|-------------|------------------|
| alice@example.com    | testpass123 | Алиса Иванова    |
| bob@example.com      | testpass123 | Боб Петров       |
| carol@example.com    | testpass123 | Каролина Сидорова |

Каждый пользователь имеет один проект для демонстрации функционала.

## Основные страницы

*   `/` — Главная страница (список всех проектов)
*   `/users/login/` — Вход
*   `/users/register/` — Регистрация
*   `/users/list/` — Список пользователей
*   `/users/<id>/` — Профиль пользователя
*   `/projects/create-project/` — Создать проект
*   `/projects/<int:pk>/` — Детальная страница проекта
*   `/projects/favorites/` — Избранные проекты

## Структура проекта

```
team_finder/          # главный Django-проект
├── projects/         # приложение: проекты (models, views, forms, urls)
├── users/            # приложение: пользователи (models, views, forms, urls)
├── templates_var1/   # HTML-шаблоны (вариант 1 — Избранное)
├── static/           # CSS, JS, изображения
├── docker-compose.yml
├── requirements.txt
└── .env_example
```

## Особенности реализации

*   Используется **вариант 1** (шаблоны `templates_var1/`): избранные проекты (сердечко), фильтрация пользователей по 4 критериям.
*   **Автоматическая генерация аватарок**: при регистрации пользователя создаётся аватарка с первой буквой имени на цветном фоне.
*   **Сортировка проектов**: по дате создания (от новых к старым).
*   **Пагинация**: 12 карточек на странице.

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

## Лицензия

MIT License
