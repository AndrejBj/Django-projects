from rest_framework import serializers        #serializers je paket koji je deo rest_framework, a rest_framework je API koji mi ovde koristimo
from .models import Drinks, Food, Alcohol

class DrinkSerializer(serializers.ModelSerializer):    #klasa DrinkSerializer ce serijalizovati klasu Drinks tj da je pretvori u neki prenosiv oblik
    class Meta:                               #meta klasa koja opisuje klasu za model Drinks
        model=Drinks
        fields=["id","name","description"]     #atribute klase Drinks
#ustvari objekte koje smo ubacili u klasu Drinks hocemo da vratimo kod nas u python kroz serijalizaciju


class FoodSerializer(serializers.ModelSerializer):    
    class Meta:                              
        model=Food
        fields=["id","name","description"]


class AlcoholSerializer(serializers.ModelSerializer):    
    class Meta:                              
        model=Alcohol
        fields=["id","name","description"]