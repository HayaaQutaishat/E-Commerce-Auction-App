# Generated by Django 4.0.4 on 2022-06-03 09:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_categories'),
    ]

    operations = [
        migrations.RenameField(
            model_name='categories',
            old_name='listing',
            new_name='listings',
        ),
    ]