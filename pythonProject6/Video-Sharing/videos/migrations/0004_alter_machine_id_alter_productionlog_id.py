# Generated by Django 4.2.11 on 2024-04-11 04:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0003_machine_productionlog'),
    ]

    operations = [
        migrations.AlterField(
            model_name='machine',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='productionlog',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
