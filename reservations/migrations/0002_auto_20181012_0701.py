# Generated by Django 2.1.2 on 2018-10-12 07:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservations',
            name='observations',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='reservations',
            name='check_in',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='reservations',
            name='check_out',
            field=models.DateField(),
        ),
    ]