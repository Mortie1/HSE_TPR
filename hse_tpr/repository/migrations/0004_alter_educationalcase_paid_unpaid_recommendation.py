# Generated by Django 4.2 on 2023-05-03 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0003_educationalcase_other_information'),
    ]

    operations = [
        migrations.AlterField(
            model_name='educationalcase',
            name='paid_unpaid_recommendation',
            field=models.BooleanField(default=None),
        ),
    ]
