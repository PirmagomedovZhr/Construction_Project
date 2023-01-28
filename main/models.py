from django.db import models
from django.contrib.auth.models import User


class Character(models.TextChoices):
    designer = 'Дизайнер'
    architector = 'Архитектор'


class Task(models.Model):
    title = models.CharField('Название', max_length=50)
    task = models.TextField('Описание')

    def __str__(self):
        return self.title


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    POSITION_CHOICES = [('architect', 'архитектор'), ('designer', 'дизайнер'), ('constructor', 'конструктор')]
    position = models.CharField(max_length=20, choices=POSITION_CHOICES)
