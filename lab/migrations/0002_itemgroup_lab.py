# Generated by Django 4.2 on 2024-04-09 05:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lab', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='itemgroup',
            name='lab',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='lab.lab'),
            preserve_default=False,
        ),
    ]