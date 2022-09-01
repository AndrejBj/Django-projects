from rest_framework import serializers
from posts.models import Post
from django.contrib.auth.models import User                          #dodamo posle ubacivanja klase za serijalizaciju usera

#kad se napravi neka klasa, mora da se serijalizacije jer se tako pretvara u prenosiv oblik
class PostSerializer(serializers.HyperlinkedModelSerializer):        #HyperlinkedModelSerializer pravi linkove, tj napravi podatak da kad ga kliknemo da nas odvede na neki link

    class Meta:                                                      #meta klasa koja opisuje klasu koja se koristi da serijalizuje Post, a posto se koristi klasa Post daje info o njoj tj njene atribute id, title, content i author
        model = Post
        fields = ['id','title','content','author']

    def create(self, validated_data):                                #ova metoda odgovara naredbi INSERT; omogucava sa metodom POST da insertujemo nesto u bazu podataka
        return Post.objects.create(**validated_data)

    def update(self, instance, validated_data):                      #metoda za update, gde cemo sa metodom PUT azurirati postojeci podatak
        instance.title = validated_data.get('title', instance.title)
        instance.content = validated_data.get('content', instance.content)
        instance.author = validated_data.get('author', instance.author)
        instance.save()
        return instance

class UserSerializer(serializers.HyperlinkedModelSerializer):        #klasa koja serijalizuje usere
    posts = serializers.HyperlinkedRelatedField(many=True, view_name='post-detail',read_only=True) 
    owner = serializers.ReadOnlyField(source='owner.username')
 
    class Meta:
        model = User
        fields = ['id', 'username', 'posts', 'owner']