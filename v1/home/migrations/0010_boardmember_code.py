# Generated by Django 4.2.6 on 2023-10-21 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0009_boardmember_is_success'),
    ]

    operations = [
        migrations.AddField(
            model_name='boardmember',
            name='code',
            field=models.CharField(default=1205, max_length=4),
            preserve_default=False,
        ),
    ]
