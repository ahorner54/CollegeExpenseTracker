# Generated by Django 5.0.2 on 2024-04-26 19:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budget', '0002_rename_expected_end_balance_semester_current_balance'),
    ]

    operations = [
        migrations.AddField(
            model_name='semester',
            name='semester_name',
            field=models.CharField(default='Fall 2024', max_length=30),
            preserve_default=False,
        ),
    ]
