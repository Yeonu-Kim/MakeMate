# Generated by Django 4.1 on 2024-02-13 07:06

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('group', '0003_alter_group_end_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='group',
            name='choice',
        ),
        migrations.RemoveField(
            model_name='group',
            name='team_number',
        ),
        migrations.RemoveField(
            model_name='group',
            name='type',
        ),
        migrations.AlterField(
            model_name='group',
            name='end_date',
            field=models.DateTimeField(default=datetime.date(2024, 2, 16)),
        ),
    ]
