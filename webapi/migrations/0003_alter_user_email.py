# Generated by Django 3.2.4 on 2021-10-28 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapi', '0002_user_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.TextField(null=True),
        ),
    ]