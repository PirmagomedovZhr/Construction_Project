from django.db import models

class Task(models.Model):
    title = models.CharField('Название', max_length=50)
    task = models.TextField('Описание')
    nomer = models.IntegerField()

    def __str__(self):
        return self.title