# Generated by Django 4.2.6 on 2023-10-17 12:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_task'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='column',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='home.column'),
        ),
    ]
