# Generated by Django 3.2.5 on 2021-11-28 07:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0011_graded_grader_sh'),
    ]

    operations = [
        migrations.AddField(
            model_name='work',
            name='weightage',
            field=models.IntegerField(null=True),
        ),
    ]
