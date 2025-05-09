# Generated by Django 5.1.7 on 2025-04-06 12:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compliance', '0004_historicalreport_technical_information_wording_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalreport',
            name='enforcement_procedure',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='historicalreport',
            name='feedback_header',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='historicalreport',
            name='legal_compliance',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='historicalreport',
            name='reporting_problems',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='historicalreport',
            name='technical_information_wording',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='report',
            name='enforcement_procedure',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='report',
            name='feedback_header',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='report',
            name='legal_compliance',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='report',
            name='reporting_problems',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='report',
            name='technical_information_wording',
            field=models.BooleanField(default=False),
        ),
    ]
