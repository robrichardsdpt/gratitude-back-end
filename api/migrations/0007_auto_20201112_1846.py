# Generated by Django 3.0 on 2020-11-12 18:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_auto_20201112_1845'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='gratitude',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='api.Gratitude'),
        ),
    ]