# Generated by Django 4.1.3 on 2022-11-21 07:53

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('stations', '0003_coordinates'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coordinates',
            name='station',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='coordinates', to='stations.station', verbose_name='Станция'),
        ),
        migrations.AlterField(
            model_name='station',
            name='status',
            field=models.CharField(choices=[('OK', 'running'), ('BR', 'broken')], max_length=32, verbose_name='Статус'),
        ),
        migrations.CreateModel(
            name='Command',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('axis', models.CharField(choices=[('X', 'X'), ('Y', 'Y'), ('Z', 'Z')], max_length=8, verbose_name='Ось')),
                ('distance', models.IntegerField(verbose_name='Расстояние')),
                ('station', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stations.station', verbose_name='Команда')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
        ),
    ]
