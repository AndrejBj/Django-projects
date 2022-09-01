from django.http import JsonResponse
from .models import Drinks, Food, Alcohol
from .serializers import DrinkSerializer, FoodSerializer, AlcoholSerializer
from rest_framework.response import Response                          #rest_framework.response je API
from rest_framework import status                                     #rest_framework je web framework
from urllib import response
from rest_framework.decorators import api_view                        #import za javascript dekorater


@api_view(["GET", "POST"])                                            #ovo se odnosi na sve objekte, pa se stavlja samo GET i POST, jer npr nema smisla stavljati DELETE i PUT za sve stavke (npr hocemo da obrisemo 1 stavku i obrisemo sve)
def drink_list(request): 
    if (request.method=="GET"):                                       #metoda koja vraca Json formatu
        drinks = Drinks.objects.all()                                 #pokupi podatke iz baze (modela)
        serializer = DrinkSerializer(drinks,many=True)                #serijalizuje ih
        #return JsonResponse({"drinks":serializer.data})              #i vrati u Json formatu, ali smo ga zakomentarisali posto smo ipak dodali lepsi format preko dekoratera i response koda u redu ispod
        return Response({"drink":serializer.data})                    #dodali umesto reda iznad za lepsi format (radi sa dekoraterom iz reda 10). Taj lepsi interfejs omogucava Response objekat
    elif(request.method=="POST"):
        serializer = DrinkSerializer(data=request.data)               #ovde nemamo objekat u zagradi za razliku od reda 32, gde za PUT naredbu imamo drink,data=request.data, sto je zbog toga sto se ovde odnosi na sve objekte
        if(serializer.is_valid()):
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)       #vraca 201 created

@api_view(["GET","PUT","DELETE"])                                     #dekorator koji daje novu funkcionalnost metodi drink_detail - dodaje get,put i delete
def drink_detail(request,id):                                         #id ovde je u urls.py unutar koda drinks/<int:id>
    try:
        drink = Drinks.objects.get(pk=id)                             #trazimo samo zadati id, za razliku od Drinks.objects.all() u redu 11 gde smo uzeli sve, ovde uzimamo samo za uneti id
    except Drinks.DoesNotExist:                                       #ako ukucamo veci broj nego sto ima objekata (npr mi napravili 2, ako ukucamo 3, izbacice not found)
        return Response(status=status.HTTP_404_NOT_FOUND)             #ako postoji taj broj objekta, vratice HTTP 200 OK sto znaci da je ok, ako ga nema, vratice HTTP_404_NOT_FOUND
    if(request.method=="GET"):                                        #ova metoda getuje (selectuje) podatke sa serveru kad ukucamo konkretno broj npr drinks/1, drinks2.. ako prodje tj ako ukucamo validan broj
        serializer = DrinkSerializer(drink)                           #izvrsi se serijalizacija
        return Response({"drink":serializer.data})                    #i vrate se (de?)serijalizovani podaci u posebnom lepsem web obliku (probaj)
    elif(request.method=="PUT"):                                      #ova metoda radi update; sad ce se pojaviti dugme PUT u desno dole na stranici 
        serializer = DrinkSerializer(drink,data=request.data)         #podatke koje vracam sa metodom put, moramo da upamtimo u neku promenljivu, zato je ovde data=request.data, request.data su ustvari podaci koje mi menjamo
        if(serializer.is_valid()):                                    #da li je serializer validan? ako jeste, save
            serializer.save()                                         #serializer.save() u prevodu znaci update, tj da se sacuvaju ti novi podaci koje smo menjali u redu 27 sa request.data; to je ustvari kao commit
            return Response(serializer.data)                          #vraca te sacuvane podatke
        return Response(serializer.error,status=status.HTTP_400_BAD_REQUEST)      #u suprotnom vraca ovaj error
    elif(request.method=="DELETE"):                                               #ova metoda radi delete;
        drink.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


def food_list(request):                                    
    food = Food.objects.all()                          
    serializer = FoodSerializer(food,many=True)          
    return JsonResponse({"food":serializer.data})

@api_view(["GET","PUT","DELETE"])
def food_detail(request,id):                              
    try:
        food = Food.objects.get(pk=id)
    except Food.DoesNotExist:                             
        return Response(status=status.HTTP_404_NOT_FOUND)
    if(request.method=="GET"):                              
        serializer = FoodSerializer(food)                
        return Response({"food":serializer.data})          
    elif(request.method=="PUT"):
        pass
    elif(request.method=="DELETE"):
        pass 


def alcohol_list(request):                                    
    alcohol = Alcohol.objects.all()                          
    serializer = AlcoholSerializer(alcohol,many=True)          
    return JsonResponse({"alcohol":serializer.data})

@api_view(["GET","PUT","DELETE"])
def alcohol_detail(request,id):                              
    try:
        alcohol = Alcohol.objects.get(pk=id)
    except Alcohol.DoesNotExist:                             
        return Response(status=status.HTTP_404_NOT_FOUND)
    if(request.method=="GET"):                              
        serializer = AlcoholSerializer(alcohol)                
        return Response({"alcohol":serializer.data})          
    elif(request.method=="PUT"):
        pass
    elif(request.method=="DELETE"):
        pass 