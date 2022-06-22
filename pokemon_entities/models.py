from django.db import models


class Pokemon(models.Model):
    title = models.CharField(
        verbose_name="Название покемона на русском", max_length=200)
    title_en = models.CharField(verbose_name="Название покемона на ангийском",
                                max_length=200, blank=True)
    title_jp = models.CharField(verbose_name="Название покемона на японском",
                                max_length=200, blank=True)
    image = models.ImageField(verbose_name="Картинка покемона",
                              blank=True, null=True)
    description = models.TextField(verbose_name="Описание", blank=True)
    previous_evolution = models.ForeignKey("self",
                                           on_delete=models.SET_NULL,
                                           verbose_name="Из кого эволюционирует",
                                           null=True,
                                           blank=True,
                                           related_name="next_evolutions")

    def __str__(self):
        return self.title


class PokemonEntity(models.Model):
    latitude = models.FloatField(verbose_name="Широта")
    longitude = models.FloatField(verbose_name="Долгота")
    pokemon_location = models.ForeignKey(Pokemon, on_delete=models.CASCADE,
                                         verbose_name="Выберите покемона")
    appeared_at = models.DateTimeField(verbose_name="Появится в: ",
                                       default=None)
    disappeared_at = models.DateTimeField(verbose_name="Исчезнет в: ",
                                          default=None)
    level = models.IntegerField(verbose_name="Уровень покемона",
                                null=True, blank=True)
    health = models.IntegerField(verbose_name="Здоровье покемона",
                                 null=True, blank=True)
    strength = models.IntegerField(verbose_name="Сила покемона",
                                   null=True, blank=True)
    defence = models.IntegerField(verbose_name="Защита покемона",
                                  null=True, blank=True)
    stamina = models.IntegerField(verbose_name="Уровень покемона",
                                  null=True, blank=True)
