# Generated by Django 4.1.2 on 2023-05-26 07:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_timespent'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectuser',
            name='due_date',
            field=models.DateField(blank=True, null=True, verbose_name='Срок завершения'),
        ),
    ]