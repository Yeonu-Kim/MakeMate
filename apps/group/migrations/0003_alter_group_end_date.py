<<<<<<< HEAD:group/migrations/0003_alter_group_end_date.py
# Generated by Django 5.0.1 on 2024-02-17 04:24
=======
# Generated by Django 4.2.9 on 2024-02-17 08:28
>>>>>>> 2dd49781a43f7fb9b680218e063dd96a938d532d:apps/group/migrations/0003_alter_group_end_date.py

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
<<<<<<< HEAD:group/migrations/0003_alter_group_end_date.py
    dependencies = [
        ("group", "0002_remove_group_choice_remove_group_team_number_and_more"),
=======

    dependencies = [
        ('group', '0002_remove_group_choice_remove_group_team_number_and_more'),
>>>>>>> 2dd49781a43f7fb9b680218e063dd96a938d532d:apps/group/migrations/0003_alter_group_end_date.py
    ]

    operations = [
        migrations.AlterField(
<<<<<<< HEAD:group/migrations/0003_alter_group_end_date.py
            model_name="group",
            name="end_date",
=======
            model_name='group',
            name='end_date',
>>>>>>> 2dd49781a43f7fb9b680218e063dd96a938d532d:apps/group/migrations/0003_alter_group_end_date.py
            field=models.DateTimeField(default=datetime.date(2024, 2, 20)),
        ),
    ]
