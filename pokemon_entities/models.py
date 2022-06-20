from django.db import models


class Pokemon(models.Model):
    title = models.CharField(max_length=200)
    title_en = models.CharField(max_length=200, blank=True)
    title_jp = models.CharField(max_length=200, blank=True)
    image = models.ImageField(blank=True, null=True)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.title


class PokemonEntity(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    pokemon_location = models.ForeignKey(Pokemon, on_delete=models.CASCADE)
    appeared_at = models.DateTimeField(default=None)
    disappeared_at = models.DateTimeField(default=None)
    level = models.IntegerField(default=None)
    health = models.IntegerField(default=None)
    strength = models.IntegerField(default=None)
    defence = models.IntegerField(default=None)
    stamina = models.IntegerField(default=None)
