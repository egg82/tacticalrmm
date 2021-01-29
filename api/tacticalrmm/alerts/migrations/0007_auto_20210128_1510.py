# Generated by Django 3.1.4 on 2021-01-28 15:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('agents', '0026_auto_20201125_2334'),
        ('alerts', '0006_auto_20210128_0417'),
    ]

    operations = [
        migrations.AddField(
            model_name='alertexclusion',
            name='agents',
            field=models.ManyToManyField(related_name='alert_exclusions', to='agents.Agent'),
        ),
        migrations.AlterField(
            model_name='alertexclusion',
            name='alert_template',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='template', to='alerts.alerttemplate'),
        ),
    ]
