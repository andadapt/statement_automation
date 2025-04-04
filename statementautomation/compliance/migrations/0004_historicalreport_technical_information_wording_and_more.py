# Generated by Django 5.1.7 on 2025-04-04 08:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compliance', '0003_historicalreport_portfolio_report_portfolio'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalreport',
            name='technical_information_wording',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='comments',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='product_owner_email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='product_owner_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='url_status',
            field=models.CharField(blank=True, choices=[('working', 'Working'), ('broken', 'Broken'), ('missing', 'Missing'), ('authentication', 'Authentication Required')], default='missing', max_length=20),
        ),
        migrations.AddField(
            model_name='report',
            name='technical_information_wording',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterUniqueTogether(
            name='product',
            unique_together={('name', 'portfolio')},
        ),
    ]
