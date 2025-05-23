import folium

from django.shortcuts import render
from .models import Pokemon, PokemonEntity
from django.utils.timezone import localtime
from django.shortcuts import get_object_or_404

MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    pokemons = Pokemon.objects.all()
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon in pokemons:
        active_pokemon_entities = pokemon.entities.filter(
            appeared_at__lte=localtime(),
            disappeared_at__gte=localtime()
        )
        for pokemon_entity in active_pokemon_entities:
            add_pokemon(
                folium_map,
                pokemon_entity.lat,
                pokemon_entity.lon,
                request.build_absolute_uri(pokemon.image.url)
            )

    pokemons_on_page = []
    for pokemon in pokemons:
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': request.build_absolute_uri(pokemon.image.url),
            'title_ru': pokemon.title_ru
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    pokemon = get_object_or_404(Pokemon, pk=pokemon_id)

    previous_evolution = pokemon.previous_evolution
    if previous_evolution:
        previous_evolution = {
            'title_ru': previous_evolution.title_ru,
            'pokemon_id': previous_evolution.pk,
            'img_url': request.build_absolute_uri(previous_evolution.image.url)
        }
    else:
        previous_evolution = None

    next_evolution = pokemon.next_evolutions.first()
    if next_evolution:
        next_evolution = {
            'title_ru': next_evolution.title_ru,
            'pokemon_id': next_evolution.pk,
            'img_url': request.build_absolute_uri(next_evolution.image.url)
        }
    else:
        next_evolution = None

    pokemon_entities = PokemonEntity.objects.filter(pokemon=pokemon)
    entities = []
    for pokemon_entity in pokemon_entities:
        entity = {
            'level': pokemon_entity.level,
            'lat': pokemon_entity.lat,
            'lon': pokemon_entity.lon
        }
        entities.append(entity)

    pokemons = {
        'pokemon_id': pokemon.pk,
        'title_ru': pokemon.title_ru,
        'title_en': pokemon.title_en,
        'title_jp': pokemon.title_jp,
        'description': pokemon.description,
        'img_url': request.build_absolute_uri(pokemon.image.url),
        'entities': entities,
        'previous_evolution': previous_evolution,
        'next_evolution': next_evolution
    }

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in pokemon_entities:
        add_pokemon(
            folium_map,
            pokemon_entity.lat,
            pokemon_entity.lon,
            request.build_absolute_uri(pokemon.image.url)
        )

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemons
    })
