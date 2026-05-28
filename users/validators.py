import re

from django.core.exceptions import ValidationError


def validate_phone(value):
    if value and not re.match(r'^(\+7|8)\d{10}$', value):
        raise ValidationError('Телефон: формат 8XXXXXXXXXX или +7XXXXXXXXXX')


def validate_github(value):
    if value and 'github.com' not in value:
        raise ValidationError('Укажите ссылку на github.com')
