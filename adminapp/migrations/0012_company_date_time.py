# Generated by Django 4.2.7 on 2024-02-19 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminapp', '0011_remove_company_date_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='date_time',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
