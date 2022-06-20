import django
import folium
import json


from django.http import HttpResponseNotFound
from django.shortcuts import render
from .models import Pokemon, PokemonEntity


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
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    pokemons = Pokemon.objects.all()
    pokemon_entities = PokemonEntity.objects.all()
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in pokemon_entities:
        if pokemon_entity.appeared_at < django.utils.timezone.localtime() < pokemon_entity.disappeared_at:
            add_pokemon(
                folium_map, pokemon_entity.latitude,
                pokemon_entity.longitude,
                request.build_absolute_uri(f'media/{pokemon_entity.pokemon_location.image}')
            )
        
        if pokemon_entity.disappeared_at < django.utils.timezone.localtime():
            pokemon_entity.delete()

    pokemons_on_page = []
    for pokemon in pokemons:
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': request.build_absolute_uri(f'media/{pokemon.image}'),
            'title_ru': pokemon.title,
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    pokemon_entities = PokemonEntity.objects.filter(pokemon_location_id = pokemon_id)
    first_pokemon_id = Pokemon.objects.filter(id=pokemon_id).first()
    
    if not pokemon_entities:
         return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')
    
    requested_pokemon = []
    
    
    for pokemon_entity in pokemon_entities:
            pokemon = {
                'img_url': request.build_absolute_uri(f'/media/{pokemon_entity.pokemon_location.image}'),
                "pokemon_id": pokemon_entity.pokemon_location_id,
                "title_ru": pokemon_entity.pokemon_location.title,
                "title_jp": pokemon_entity.pokemon_location.title_jp,
                "title_en": pokemon_entity.pokemon_location.title_en,
                'entities': 
                {'lat': pokemon_entity.latitude,
                'lon': pokemon_entity.longitude,
                },
                'description': pokemon_entity.pokemon_location.description,
            }

            if first_pokemon_id.previous_evolution:
                pokemon['previous_evolution'] = {
                "title_ru": first_pokemon_id.previous_evolution.title,
                "pokemon_id": first_pokemon_id.previous_evolution.id,
                "img_url":  request.build_absolute_uri(f'/media/{first_pokemon_id.previous_evolution.image}')
                }

            requested_pokemon.append(pokemon)

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    
    for pokemon_entity in requested_pokemon:
        add_pokemon(
            folium_map, pokemon_entity['entities']['lat'],
            pokemon_entity['entities']['lon'],
            pokemon['img_url'],
        )

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemon
    })
