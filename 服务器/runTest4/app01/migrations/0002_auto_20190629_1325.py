# Generated by Django 2.1.4 on 2019-06-29 05:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user2',
            old_name='id',
            new_name='email',
        ),
    ]
