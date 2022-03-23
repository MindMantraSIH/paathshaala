# Generated by Django 4.0.3 on 2022-03-23 17:50

import autoslug.fields
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Data',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('levelc', models.IntegerField(max_length=100)),
                ('disc_content', models.CharField(max_length=5000)),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from='disc_title', unique=True)),
                ('school', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='profiles.school')),
            ],
        ),
    ]
