# Generated by Django 4.1.5 on 2023-03-12 16:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('statuses', '0002_alter_statuses_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='status',
            name='name',
            field=models.CharField(max_length=255, unique=True, verbose_name='Name'),
        ),
    ]
