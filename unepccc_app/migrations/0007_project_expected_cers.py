# Generated by Django 4.1.3 on 2022-12-01 08:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('unepccc_app', '0006_remove_project_project_idval'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='expected_CERs',
            field=models.IntegerField(default=0),
        ),
    ]