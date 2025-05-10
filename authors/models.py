from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Profile(models.Model):
    author = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    bio = models.TextField(default='', blank=True)

    def __str__(self):
        return f'{self.author.username}'
