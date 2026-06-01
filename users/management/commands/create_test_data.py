from django.core.management.base import BaseCommand
from django.db import IntegrityError

from projects.models import Project
from users.models import User


TEST_USERS = [
    {
        'email': 'alice@example.com',
        'name': 'Алиса',
        'surname': 'Иванова',
        'phone': '+79001112233',
        'password': 'testpass123',
    },
    {
        'email': 'bob@example.com',
        'name': 'Боб',
        'surname': 'Петров',
        'phone': '+79004445566',
        'password': 'testpass123',
    },
    {
        'email': 'carol@example.com',
        'name': 'Каролина',
        'surname': 'Сидорова',
        'phone': '+79007778899',
        'password': 'testpass123',
    },
]

TEST_PROJECTS = [
    {
        'name': 'Team Finder Backend',
        'description': 'Разработка бэкенда для платформы поиска команды.',
        'status': Project.STATUS_OPEN,
        'owner_email': 'alice@example.com',
    },
    {
        'name': 'Mobile App',
        'description': 'Мобильное приложение для iOS и Android.',
        'status': Project.STATUS_OPEN,
        'owner_email': 'bob@example.com',
    },
    {
        'name': 'Data Science Dashboard',
        'description': 'Дашборд для визуализации данных.',
        'status': Project.STATUS_OPEN,
        'owner_email': 'carol@example.com',
    },
]


class Command(BaseCommand):
    help = 'Создаёт тестовых пользователей и проекты для демонстрации'

    def handle(self, *args, **kwargs):
        users = {}
        for data in TEST_USERS:
            try:
                user = User.objects.create_user(
                    email=data['email'],
                    password=data['password'],
                    name=data['name'],
                    surname=data['surname'],
                    phone=data['phone'],
                )
                users[data['email']] = user
                self.stdout.write(self.style.SUCCESS(f'Создан пользователь: {data["email"]}'))
            except IntegrityError:
                users[data['email']] = User.objects.get(email=data['email'])
                self.stdout.write(f'Пользователь уже существует: {data["email"]}')

        for data in TEST_PROJECTS:
            owner = users.get(data['owner_email'])
            if owner and not Project.objects.filter(name=data['name']).exists():
                Project.objects.create(
                    name=data['name'],
                    description=data['description'],
                    status=data['status'],
                    owner=owner,
                )
                self.stdout.write(self.style.SUCCESS(f'Создан проект: {data["name"]}'))
            else:
                self.stdout.write(f'Проект уже существует: {data["name"]}')

        self.stdout.write(self.style.SUCCESS('Тестовые данные успешно загружены'))
