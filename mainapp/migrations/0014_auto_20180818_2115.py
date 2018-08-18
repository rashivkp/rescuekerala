# Generated by Django 2.0.7 on 2018-08-18 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0013_merge_20180818_2011'),
    ]

    operations = [
        migrations.AlterField(
            model_name='victim',
            name='contact',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='victim',
            name='coordinates',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='victim',
            name='degree_of_emergency',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='victim',
            name='done',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='victim',
            name='help_required_immediatly',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='victim',
            name='location',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='victim',
            name='no_of_people',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='victim',
            name='status',
            field=models.TextField(blank=True, null=True),
        ),
    ]
