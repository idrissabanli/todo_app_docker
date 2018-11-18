# Generated by Django 2.1.2 on 2018-11-01 09:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0005_tasks_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tasks',
            name='status',
            field=models.CharField(choices=[('s', 'Starting'), ('r', 'Running'), ('c', 'Complated')], default='s', max_length=1, verbose_name='Status'),
        ),
    ]
