from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from projects.models import Project

User = get_user_model()

USERS = [
    {'email': 'maria@yandex.ru', 'name': 'Мария',   'surname': 'Иванова',  'password': 'password'},
    {'email': 'alex@yandex.ru',  'name': 'Алексей', 'surname': 'Петров',   'password': 'password'},
    {'email': 'olga@yandex.ru',  'name': 'Ольга',   'surname': 'Смирнова', 'password': 'password'},
]

PROJECTS = [
    {'owner': 'maria@yandex.ru', 'name': 'Планировщик задач',
     'description': 'Веб-приложение для управления задачами с Kanban-доской.', 'status': 'open'},
    {'owner': 'maria@yandex.ru', 'name': 'Рецепты онлайн',
     'description': 'Платформа для публикации и поиска кулинарных рецептов.', 'status': 'open'},
    {'owner': 'alex@yandex.ru',  'name': 'Трекер привычек',
     'description': 'Мобильное приложение для отслеживания полезных привычек.', 'status': 'open'},
    {'owner': 'alex@yandex.ru',  'name': 'Telegram-бот для RSS',
     'description': 'Бот для автоматической рассылки новостей из RSS-лент.', 'status': 'closed'},
    {'owner': 'olga@yandex.ru',  'name': 'Онлайн-портфолио',
     'description': 'Генератор красивых портфолио для разработчиков.', 'status': 'open'},
    {'owner': 'olga@yandex.ru',  'name': 'Сервис коротких ссылок',
     'description': 'Аналог bit.ly с аналитикой переходов.', 'status': 'open'},
]


class Command(BaseCommand):
    help = 'Создаёт тестовых пользователей и проекты'

    def handle(self, *args, **options):
        users = {}
        for u in USERS:
            obj, created = User.objects.get_or_create(
                email=u['email'],
                defaults={'name': u['name'], 'surname': u['surname']}
            )
            if created:
                obj.set_password(u['password'])
                obj.save()
                self.stdout.write(f'  + {obj.email}')
            else:
                self.stdout.write(f'  = {obj.email} (уже существует)')
            users[u['email']] = obj

        for p in PROJECTS:
            proj, created = Project.objects.get_or_create(
                name=p['name'], owner=users[p['owner']],
                defaults={'description': p['description'], 'status': p['status']}
            )
            if created:
                self.stdout.write(f'  + проект: {proj.name}')

        self.stdout.write(self.style.SUCCESS('Готово!'))
