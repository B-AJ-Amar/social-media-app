# Generated by Django 4.2.2 on 2023-07-09 18:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0007_alter_reaction_user_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='is_archived',
        ),
    ]
