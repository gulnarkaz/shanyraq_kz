# Generated by Django 5.1.7 on 2025-04-01 10:23

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Shanyrak',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('sale', 'Продажа'), ('rent', 'Аренда')], max_length=10)),
                ('price', models.DecimalField(decimal_places=2, max_digits=15)),
                ('address', models.CharField(max_length=255)),
                ('area', models.DecimalField(decimal_places=1, max_digits=5)),
                ('rooms_count', models.IntegerField()),
                ('description', models.TextField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shanyraks', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('shanyrak', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='core.shanyrak')),
            ],
        ),
    ]
