# Generated by Django 4.2.8 on 2023-12-29 05:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('snippets', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='snippet',
            old_name='upodate_at',
            new_name='update_at',
        ),
    ]