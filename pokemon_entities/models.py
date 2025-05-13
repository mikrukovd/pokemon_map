from django.db import models


class Pokemon(models.Model):
    title_ru = models.CharField(
        max_length=200,
        verbose_name='Название покемона ru'
    )
    title_en = models.CharField(
        max_length=200,
        verbose_name='Название покемона en'
    )
    title_jp = models.CharField(
        max_length=200,
        verbose_name='Название покемона jp'
    )
    image = models.ImageField(
        upload_to='pokemon_images/',
        blank=True,
        verbose_name='Загрузить изображение'
    )
    description = models.CharField(
        max_length=1000,
        verbose_name='Описание'
    )
    previous_evolution = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='next_evolution',
        verbose_name='Эволюция покемона'
    )

    def __str__(self):
        return f'{self.title_ru}'


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(
        Pokemon,
        on_delete=models.CASCADE,
        related_name='pokemon_entities',
        verbose_name='Покемон'
    )
    lat = models.FloatField(verbose_name='Широта')
    lon = models.FloatField(verbose_name='Долгота')
    appeared_at = models.DateTimeField(verbose_name='Дата появления')
    disappeared_at = models.DateTimeField(verbose_name='Дата исчезновения')
    level = models.IntegerField(
        blank=True,
        null=True,
        verbose_name='Уровень'
    )
    health = models.IntegerField(
        blank=True,
        null=True,
        verbose_name='Количество жизни'
    )
    strength = models.IntegerField(
        blank=True,
        null=True,
        verbose_name='Сила'
    )
    defence = models.IntegerField(
        blank=True,
        null=True,
        verbose_name='Защита'
    )
    stamina = models.IntegerField(
        blank=True,
        null=True,
        verbose_name='Выносливость'
    )

    def __str__(self):
        return f'{self.pokemon.title_ru}'
