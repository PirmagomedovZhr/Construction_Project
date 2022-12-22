from django.db import models

class Task(models.Model):
    title = models.CharField('Название', max_length=50)
    task = models.TextField('Описание')

    def __str__(self):
        return self.title

class Doljn(models.Model):

    FRESHMAN = 'AR'
    SOPHOMORE = 'KS'
    JUNIOR = 'DZ'
    YEAR_IN_SCHOOL_CHOICES = [
        (FRESHMAN, 'Архитектор'),
        (SOPHOMORE, 'Конструктор'),
        (JUNIOR, 'Дизайнер'),
    ]
    year_in_school = models.CharField(
        max_length=2,
        choices=YEAR_IN_SCHOOL_CHOICES,
        default=FRESHMAN,
    )


