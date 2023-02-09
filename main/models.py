from django.db import models
from django.contrib.auth.models import User, AbstractUser



class CustomUser(AbstractUser):
    positions = (
        ('architect', 'архитектор'),
        ('construction', 'конструктор'),
        ('designer', 'дизайнер')
    )

    position = models.CharField('Должность', max_length=12, choices=positions, default='')

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    POSITION_CHOICES = [('architect', 'архитектор'), ('designer', 'дизайнер'), ('constructor', 'конструктор')]
    position = models.CharField(max_length=20, choices=POSITION_CHOICES)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    position = models.CharField(max_length=20, choices=[
            ('Архитектор', 'architect'),
            ('Конструктор', 'constructor'),
            ('Дизайнер', 'designer')
        ])
    def __str__(self):
        return self.position


class Task(models.Model):
    title = models.CharField('Название', max_length=50)
    task = models.TextField('Описание')

    def __str__(self):
        return self.title


