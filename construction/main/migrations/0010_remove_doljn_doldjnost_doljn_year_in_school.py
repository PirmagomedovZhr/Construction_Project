# Generated by Django 4.1.2 on 2022-12-22 09:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_remove_doljn_title_doljn_doldjnost'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='doljn',
            name='Doldjnost',
        ),
        migrations.AddField(
            model_name='doljn',
            name='year_in_school',
            field=models.CharField(choices=[('AR', 'Архитектор'), ('KS', 'Конструктор'), ('DZ', 'Дизайнер')], default='AR', max_length=2),
        ),
    ]
