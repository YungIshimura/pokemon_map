# Generated by Django 3.1.14 on 2022-06-22 06:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_entities', '0011_auto_20220622_0624'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pokemonentity',
            old_name='pokemon_location',
            new_name='pokemon',
        ),
    ]