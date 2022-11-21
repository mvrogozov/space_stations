from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Station(models.Model):
    CHOICES = (
        ('OK', 'running'),
        ('BR', 'broken')
    )

    name = models.CharField(
        'Имя',
        max_length=254,
        unique=True,
        null=False
    )
    status = models.CharField(
        max_length=32,
        choices=CHOICES,
        verbose_name='Статус'
    )
    create_date = models.DateTimeField(
        'Дата создания',
        auto_now_add=True
    )
    brake_date = models.DateTimeField(
        'Дата поломки',
        null=True,
        blank=True
    )

    def __str__(self):
        return self.name


class Coordinates(models.Model):
    x = models.IntegerField(default=100)
    y = models.IntegerField(default=100)
    z = models.IntegerField(default=100)
    station = models.OneToOneField(
        Station,
        on_delete=models.CASCADE,
        related_name='coordinates',
        verbose_name='Станция'
    )

    def __str__(self):
        return f'{self.x},{self.y},{self.z}'


class Command(models.Model):
    CHOICES = (
        ('x', 'x'),
        ('y', 'y'),
        ('z', 'z')
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    axis = models.CharField(
        choices=CHOICES,
        max_length=8,
        verbose_name='Ось'
    )
    distance = models.IntegerField(
        'Расстояние'
    )
    station = models.ForeignKey(
        Station,
        on_delete=models.CASCADE,
        verbose_name='Станция'
    )

    def __str__(self):
        return f'{self.user} - {self.station.name}'
