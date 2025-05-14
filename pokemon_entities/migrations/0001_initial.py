import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Pokemon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title_ru', models.CharField(max_length=200, verbose_name='Название покемона ru')),
                ('title_en', models.CharField(blank=True, max_length=200, verbose_name='Название покемона en')),
                ('title_jp', models.CharField(blank=True, max_length=200, verbose_name='Название покемона jp')),
                ('image', models.ImageField(blank=True, upload_to='pokemon_images/', verbose_name='Загрузить изображение')),
                ('description', models.TextField(verbose_name='Описание')),
                ('previous_evolution', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='next_evolutions', to='pokemon_entities.pokemon', verbose_name='Эволюция покемона')),
            ],
        ),
        migrations.CreateModel(
            name='PokemonEntity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lat', models.FloatField(blank=True, verbose_name='Широта')),
                ('lon', models.FloatField(blank=True, verbose_name='Долгота')),
                ('appeared_at', models.DateTimeField(verbose_name='Дата появления')),
                ('disappeared_at', models.DateTimeField(verbose_name='Дата исчезновения')),
                ('level', models.IntegerField(blank=True, null=True, verbose_name='Уровень')),
                ('health', models.IntegerField(blank=True, null=True, verbose_name='Количество жизни')),
                ('strength', models.IntegerField(blank=True, null=True, verbose_name='Сила')),
                ('defence', models.IntegerField(blank=True, null=True, verbose_name='Защита')),
                ('stamina', models.IntegerField(blank=True, null=True, verbose_name='Выносливость')),
                ('pokemon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='entities', to='pokemon_entities.pokemon', verbose_name='Покемон')),
            ],
        ),
    ]
