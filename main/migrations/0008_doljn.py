# Generated by Django 4.1.2 on 2022-12-22 09:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_delete_role'),
    ]

    operations = [
        migrations.CreateModel(
            name='Doljn',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='Название')),
            ],
        ),
    ]