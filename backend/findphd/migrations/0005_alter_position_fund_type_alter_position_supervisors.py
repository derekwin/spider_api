# Generated by Django 4.0.6 on 2022-07-21 06:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('findphd', '0004_alter_position_academy_alter_position_college_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='position',
            name='fund_type',
            field=models.CharField(blank=True, max_length=80, null=True),
        ),
        migrations.AlterField(
            model_name='position',
            name='supervisors',
            field=models.CharField(blank=True, max_length=80, null=True),
        ),
    ]