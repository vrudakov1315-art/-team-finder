import re
from io import BytesIO

from PIL import Image, ImageDraw, ImageFont
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.files.base import ContentFile
from django.db import models

from .constants import AVATAR_PALETTE, AVATAR_SIZE, AVATAR_FONT_SIZE, USER_NAME_MAX_LENGTH as NAME_MAX_LENGTH, USER_PHONE_MAX_LENGTH as PHONE_MAX_LENGTHfrom .managers import UserManager
from .validators import validate_github, validate_phone
from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField('Имя', max_length=NAME_MAX_LENGTH, blank=True)
    surname = models.CharField('Фамилия', max_length=NAME_MAX_LENGTH, blank=True)
    avatar = models.ImageField('Аватар', upload_to='avatars/', blank=True)
    phone = models.CharField(
        'Телефон', max_length=PHONE_MAX_LENGTH, blank=True, null=True, unique=True,
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

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('users:detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        if not self.pk and not self.avatar:
            self._generate_avatar()
        super().save(*args, **kwargs)

    def _generate_avatar(self):
        letter = (self.name[0] if self.name else self.email[0]).upper()
        color = AVATAR_PALETTE[ord(letter) % len(AVATAR_PALETTE)]
        img = Image.new('RGB', (AVATAR_SIZE, AVATAR_SIZE), color)
        draw = ImageDraw.Draw(img)
        try:
            font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', AVATAR_FONT_SIZE)
        except Exception:
            font = ImageFont.load_default()
        bbox = draw.textbbox((0, 0), letter, font=font)
        w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
        draw.text(
            ((AVATAR_SIZE - w) / 2 - bbox[0], (AVATAR_SIZE - h) / 2 - bbox[1]),
            letter, fill='white', font=font
        )
        buf = BytesIO()
        img.save(buf, format='PNG')
        safe = re.sub(r'[@.]', '_', self.email)
        self.avatar.save(f'avatar_{safe}.png', ContentFile(buf.getvalue()), save=False)
