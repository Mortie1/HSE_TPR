# Generated by Django 4.2 on 2023-04-24 10:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='educationalcase',
            name='case_department',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='case_department', to='repository.department'),
        ),
        migrations.AlterField(
            model_name='educationalcase',
            name='case_platform',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='repository.platform'),
        ),
        migrations.AlterField(
            model_name='educationalcase',
            name='educational_specialties',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='educationalcase',
            name='information_author_department',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='information_author_department', to='repository.department'),
        ),
        migrations.RemoveField(
            model_name='educationalcase',
            name='other_specs',
        ),
        migrations.AlterField(
            model_name='educationalcase',
            name='physical_authors',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='educationalcase',
            name='problems',
            field=models.TextField(blank=True),
        ),
        migrations.RemoveField(
            model_name='educationalcase',
            name='state_specs',
        ),
        migrations.AddField(
            model_name='educationalcase',
            name='other_specs',
            field=models.ManyToManyField(blank=True, to='repository.otherspec'),
        ),
        migrations.AddField(
            model_name='educationalcase',
            name='state_specs',
            field=models.ManyToManyField(blank=True, to='repository.statespec'),
        ),
    ]
