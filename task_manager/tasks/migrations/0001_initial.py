# Generated by Django 4.1.5 on 2023-02-27 07:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('statuses', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Tasks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=255)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('executor', models.CharField(max_length=255)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('status', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='statuses.status')),
            ],
        ),
    ]
