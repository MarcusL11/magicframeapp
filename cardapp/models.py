from django.db import models


# Create your models here
# https://api.scryfall.com/cards/named?fuzzy=[Derevi + Empyrial+Tactician]
class Card(models.Model):
    id = models.CharField(
        max_length=100, primary_key=True
    )  # oracle_id use to match with the ruling model.
    name = models.CharField(max_length=200, null=True)  # name
    released_at = models.DateField(null=True)  # released_at
    last_updated = models.DateField(null=True)  # last_updated

    def __str__(self):
        return self.name


# https://api.scryfall.com/cards/named?fuzzy=[Derevi + Empyrial+Tactician]
class Prices(models.Model):
    card = models.OneToOneField(Card, on_delete=models.CASCADE)
    usd = models.FloatField(null=True)  # prices/usd
    usd_foil = models.FloatField(null=True)  # prices/usd_foil
    usd_etched = models.FloatField(null=True)  # prices/usd_etched
    eur = models.FloatField(null=True)  # prices/eur
    eur_foil = models.FloatField(null=True)  # prices/eur_foil
    tix = models.FloatField(null=True)  # prices/tix


# https://api.scryfall.com/cards/named?fuzzy=[Derevi + Empyrial+Tactician] > rulings_uri
class Rulings(models.Model):
    card = models.OneToOneField(Card, on_delete=models.CASCADE)
    source = models.CharField(max_length=200, null=True)  # data/source
    published_at = models.DateField(null=True)  # data/published_at
    comment = models.TextField(null=True)  # data/comment


class CardImage(models.Model):
    card = models.OneToOneField(Card, on_delete=models.CASCADE)
    small_image = models.URLField(max_length=200, null=True)  # image_urils/small
    normal_image = models.URLField(max_length=200, null=True)  # image_urils/normal
    large_image = models.URLField(max_length=200, null=True)  # image_urils/large
    png_image = models.URLField(max_length=200, null=True)  # image_urils/png
    art_crop_image = models.URLField(max_length=200, null=True)  # image_urils/art_crop
    border_crop_image = models.URLField(
        max_length=200, null=True
    )  # image_urils/border_crop
