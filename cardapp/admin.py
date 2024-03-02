from django.contrib import admin
from .models import Card, CardImage, Prices, Rulings

# Register your models here.
admin.site.register(Card)
admin.site.register(CardImage)
admin.site.register(Prices)
admin.site.register(Rulings)
