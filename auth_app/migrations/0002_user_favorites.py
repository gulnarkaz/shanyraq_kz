# Generated by Django 5.1.7 on 2025-04-02 10:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth_app', '0001_initial'),
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='favorites',
            field=models.ManyToManyField(related_name='favorited_by', to='core.shanyrak'),
        ),
    ]
