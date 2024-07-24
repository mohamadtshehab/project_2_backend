# Generated by Django 5.0.6 on 2024-07-24 19:24

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_2_backend_api', '0002_alter_tdmodel_description_alter_tdmodel_textures'),
    ]

    operations = [
        migrations.AddField(
            model_name='tdmodel',
            name='type',
            field=models.CharField(choices=[('room', 'Room'), ('object', 'Object')], default=django.utils.timezone.now, max_length=150),
            preserve_default=False,
        ),
    ]
