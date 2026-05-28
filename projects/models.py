from django.db import models
from django.conf import settings


class Project(models.Model):
    STATUS_OPEN = 'open'
    STATUS_CLOSED = 'closed'
    STATUS_CHOICES = [
        (STATUS_OPEN, 'Открытый'),
        (STATUS_CLOSED, 'Закрытый'),
    ]

    name = models.CharField('Название', max_length=200)
    description = models.TextField('Описание', blank=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='owned_projects',
        verbose_name='Владелец'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    github_url = models.URLField('GitHub', blank=True)
    status = models.CharField('Статус', max_length=6, choices=STATUS_CHOICES, default=STATUS_OPEN)
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name='participated_projects',
        verbose_name='Участники'
    )

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'
        ordering = ['-created_at']

    def __str__(self):
        return self.name
