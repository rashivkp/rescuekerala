# Generated by Django 2.0.7 on 2018-08-18 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0013_auto_20180818_2124'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='service_group',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
