import re
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile


def validate_phone(value):
    if value and not re.match(r'^(\+7|8)\d{10}$', value):
        raise ValidationError('Телефон: формат 8XXXXXXXXXX или +7XXXXXXXXXX')


def validate_github(value):
    if value and 'github.com' not in value:
        raise ValidationError('Укажите ссылку на github.com')


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra):
        if not email:
            raise ValueError('Email обязателен')
        user = self.model(email=self.normalize_email(email), **extra)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra):
        extra.setdefault('is_staff', True)
        extra.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField('Имя', max_length=124, blank=True)
    surname = models.CharField('Фамилия', max_length=124, blank=True)
    avatar = models.ImageField('Аватар', upload_to='avatars/', blank=True)
    phone = models.CharField(
        'Телефон', max_length=12, blank=True, null=True, unique=True,
        validators=[validate_phone]
    )
    github_url = models.URLField('GitHub', blank=True, validators=[validate_github])
    about = models.TextField('О себе', max_length=256, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    favorites = models.ManyToManyField(
        'projects.Project',
        blank=True,
        related_name='interested_users',
        verbose_name='Избранное'
    )

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['-date_joined']

    def __str__(self):
        return self.email

    def get_full_name(self):
        parts = [p for p in [self.name, self.surname] if p]
        return ' '.join(parts) if parts else self.email

    def save(self, *args, **kwargs):
        if not self.pk and not self.avatar:
            self._generate_avatar()
        super().save(*args, **kwargs)

    def _generate_avatar(self):
        letter = (self.name[0] if self.name else self.email[0]).upper()
        palette = ['#01696f','#4f98a3','#6daa45','#da7101','#a86fdf','#d19900','#dd6974','#006494']
        color = palette[ord(letter) % len(palette)]
        size = 200
        img = Image.new('RGB', (size, size), color)
        draw = ImageDraw.Draw(img)
        try:
            font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 80)
        except Exception:
            font = ImageFont.load_default()
        bbox = draw.textbbox((0, 0), letter, font=font)
        w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
        draw.text(((size - w) / 2 - bbox[0], (size - h) / 2 - bbox[1]), letter, fill='white', font=font)
        buf = BytesIO()
        img.save(buf, format='PNG')
        safe = self.email.replace('@', '_').replace('.', '_')
        self.avatar.save(f'avatar_{safe}.png', ContentFile(buf.getvalue()), save=False)
