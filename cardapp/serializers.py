from rest_framework import serializers
from .models import Card, Prices, CardImage, Rulings


class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = "__all__"


class PricesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prices
        fields = "__all__"


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = (CardImage,)
        fields = "__all__"


class RulingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = (Rulings,)
        fields = "__all__"
