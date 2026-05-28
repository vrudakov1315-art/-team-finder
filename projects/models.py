from django.conf import settings
from django.db import models
from django.urls import reverse

from projects.constants import PROJECT_NAME_MAX_LENGTH


class Project(models.Model):
    STATUS_OPEN = 'open'
    STATUS_CLOSED = 'closed'
    STATUS_CHOICES = [
        (STATUS_OPEN, 'Открытый'),
        (STATUS_CLOSED, 'Закрытый'),
    ]

    name = models.CharField('Название', max_length=PROJECT_NAME_MAX_LENGTH)
    description = models.TextField('Описание', blank=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='owned_projects',
        verbose_name='Владелец'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    github_url = models.URLField('GitHub', blank=True)
    status = models.CharField(
        'Статус',
        max_length=max(len(choice) for choice in (STATUS_OPEN, STATUS_CLOSED)),
        choices=STATUS_CHOICES,
        default=STATUS_OPEN
    )
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

    def get_absolute_url(self):
        return reverse('projects:project_detail', kwargs={'pk': self.pk})
