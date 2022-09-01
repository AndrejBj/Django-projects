from django.shortcuts import render
from rest_framework import generics                #generics je klasa koja nam pojednostavljuje kod, pa cemo lakse odraditi nesto
from posts.serializers import PostSerializer
from posts.models import Post
from rest_framework.response import Response       #dodato nakon kreiranja superusera (za navigaciju)
from django.contrib.auth.models import User        #dodato nakon kreiranja superusera (za autentikaciju)
from posts.serializers import UserSerializer       #dodato nakon kreiranja superusera (za autentikaciju)
from rest_framework import permissions             #dodato nakon kreiranja superusera (za autentikaciju)
from posts.permissions import IsOwnerOrReadOnly    #dodato nakon kreiranja superusera (za autentikaciju)
from rest_framework.decorators import api_view     #dodato nakon kreiranja superusera (za navigaciju)
from rest_framework.reverse import reverse         #dodato nakon kreiranja superusera (za navigaciju)

# Create your views here.
class PostList(generics.ListCreateAPIView):        #ListCreateAPIView je klasa koja omoguci da sa naredbom Post.objects.all() kupimo sve objekte (ne moramo da pisemo kod za GET kao prosli put)
    queryset = Post.objects.all()                  #igra ulogu GET-a, vraca sve objekte (ili vraca pojedinacan objekat za dati id tog objekta)
    serializer_class = PostSerializer              #klasa za serijalizaciju
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]     #ako si autentifikovan mozes da postujes, deletujes i citas, ako nisi onda mozes samo da citas (ne moze nista da se menja)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class PostDetail(generics.RetrieveUpdateDestroyAPIView):    #klasa za id path u linku
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]   #meru autentikacije imamo i ovde, ali za razliku od reda 17 gde je za celu listu, ovde je samo po jednom objektu


@api_view(['GET'])                                          #dodato za navigaciju gde vraca response o userima i o postovima
def api_root(request, format=None):                  
    return Response({
        'users': reverse('user-list', request=request, format=format),   #drugi request odavde je request iz api_root(request, format=None), isto vazi i za format gde smo stavili da je None, nema formatiranja
        'posts': reverse('post-list', request=request, format=format)
    })


class UserList(generics.ListAPIView):               #klasa usera za autentikaciju
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveAPIView):         #klasa usera za autentikaciju
    queryset = User.objects.all()
    serializer_class = UserSerializer