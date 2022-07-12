import folium


from django.utils import timezone
from django.http import HttpResponseNotFound
from django.shortcuts import render
from .models import Pokemon, PokemonEntity


MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def add_pokemon(folium_map, lat, lon, level, health, strength, defence,
                stamina, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        icon=icon,
        popup=f'''Уровень:{level}
                  Здоровье:{health}
                  Сила:{strength}
                  Защита:{defence}
                  Выносливость{stamina}
                  '''
    ).add_to(folium_map)


def show_all_pokemons(request):
    pokemons = Pokemon.objects.all()
    pokemon_entities = PokemonEntity.objects.filter(
        appeared_at__lt=timezone.now(), disappeared_at__gt=timezone.now())
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in pokemon_entities:
        add_pokemon(
            folium_map, pokemon_entity.latitude,
            pokemon_entity.longitude,
            pokemon_entity.level,
            pokemon_entity.health,
            pokemon_entity.strength,
            pokemon_entity.defence,
            pokemon_entity.stamina,
            request.build_absolute_uri(pokemon_entity.pokemon.image.url)
        )
    pokemons_on_page = []
    for pokemon in pokemons:
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': pokemon.image.url,
            'title_ru': pokemon.title,
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    pokemon = Pokemon.objects.filter(id=pokemon_id).first()
    pokemon_entities = pokemon.entities.filter(pokemon_id=pokemon_id)
    next_pokemon = pokemon.next_evolutions.all().first()

    if not pokemon:
        return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')

    requested_pokemon = []

    for pokemon_entity in pokemon_entities:
        pokemon_params = {
            'img_url': request.build_absolute_uri(
                pokemon_entity.pokemon.image.url),
            "pokemon_id": pokemon_entity.pokemon_id,
            "title_ru": pokemon_entity.pokemon.title,
            "title_jp": pokemon_entity.pokemon.title_jp,
            "title_en": pokemon_entity.pokemon.title_en,
            'entities': {'lat': pokemon_entity.latitude,
                         'lon': pokemon_entity.longitude},
            'description': pokemon_entity.pokemon.description,
            'Уровень': pokemon_entity.level,
            'Здоровье': pokemon_entity.health,
            'Сила': pokemon_entity.strength,
            'Защита': pokemon_entity.defence,
            'Выносливость': pokemon_entity.stamina,
        }
        
        element_type = []
        
        for element in pokemon_entity.pokemon.element_type.all():
            element_type.append({
                'title': element.title,
                'img': request.build_absolute_uri(element.image.url)
            })
        
        pokemon_params['element_type'] = element_type
            
        if next_pokemon:
            pokemon_params['next_evolution'] = {
                "title_ru": next_pokemon.title,
                "pokemon_id": next_pokemon.id,
                "img_url": next_pokemon.image.url
            }

        if pokemon.previous_evolution:
            pokemon_params['previous_evolution'] = {
                "title_ru": pokemon.previous_evolution.title,
                "pokemon_id": pokemon.previous_evolution.id,
                "img_url":  pokemon.previous_evolution.image.url,
            }

        requested_pokemon.append(pokemon_params)

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)

    for pokemon_entity in requested_pokemon:
        add_pokemon(
            folium_map, pokemon_entity['entities']['lat'],
            pokemon_entity['entities']['lon'],
            pokemon_entity['Уровень'],
            pokemon_entity['Здоровье'],
            pokemon_entity['Сила'],
            pokemon_entity['Защита'],
            pokemon_entity['Выносливость'],
            pokemon_params['img_url'],
        )

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemon_params
    })
