# Generated by Django 3.1.14 on 2022-06-20 00:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_entities', '0005_pokemon_descripton'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pokemon',
            old_name='descripton',
            new_name='description',
        ),
    ]