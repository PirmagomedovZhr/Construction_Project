# Generated by Django 4.1.2 on 2023-05-26 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_projectuser_due_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='timespent',
            name='description',
            field=models.TextField(default=213123),
            preserve_default=False,
        ),
    ]
