# Generated by Django 5.0.6 on 2024-06-30 19:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('writer', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='content',
            field=models.TextField(max_length=10000),
        ),
    ]