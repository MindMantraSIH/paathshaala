# Generated by Django 4.0.3 on 2022-03-23 17:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('profiles', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('feed', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='school',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profiles.school'),
        ),
        migrations.AddField(
            model_name='post',
            name='upvote',
            field=models.ManyToManyField(blank=True, related_name='like', to=settings.AUTH_USER_MODEL),
        ),
    ]
