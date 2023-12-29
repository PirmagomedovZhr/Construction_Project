from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    positions = (
        ('Архитектор', 'архитектор'),
        ('Конструктор', 'конструктор'),
        ('Дизайнер', 'дизайнер')
    )

    position = models.CharField('Должность', max_length=12, choices=positions, default='')



class Project(models.Model):
    title = models.CharField('Название', max_length=50)
    task = models.TextField('Описание')
    is_archived = models.BooleanField('В архиве', default=False)

    def __str__(self):
        return self.title



class ProjectUser(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    due_date = models.DateField('Срок завершения', null=True, blank=True)

class TimeSpent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    date = models.DateField()
    hours_spent = models.IntegerField()
    description = models.TextField()


class ProjectFile(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='files')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='project_files/')
    description = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.project.title} - {self.file.name}"
