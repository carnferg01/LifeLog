# Generated by Django 5.0.6 on 2024-06-23 15:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('health', '0002_illness_calculated_illness'),
    ]

    operations = [
        migrations.RenameField(
            model_name='illness',
            old_name='notes',
            new_name='description',
        ),
        migrations.RenameField(
            model_name='injury',
            old_name='notes',
            new_name='description',
        ),
    ]