from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse                    #reverse upucuje na url
from django.contrib.auth import authenticate, login, logout


# Create your views here.
def index(request):                                #index metoda koju smo napravili da nas preusmerava na login metodu
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))     #ako korisnik nije autentifikovan, onda ga redirektuje na login stranu 
    return render(request, "users/user.html")             #ako jeste autentifikovan onda ide na user.html stranu

def login_view(request):                           #metoda za login koja koristi login.html fajl
    if request.method == "POST":
        username = request.POST["username"]        #prvo se kupi podaci iz forme tj iz mesta gde ubacujemo username (ovde) i password (red ispod). Logovanje iz forme je preko POST
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)     #authenticate je ugradjena metoda koja proverava da li imamo usera sa tim username i passwordom. Ako ga nema, user ce biti None
        if user is not None:                                                   #ako user postoji
            login(request, user)                                               #onda koristimo ugradjenu login metodu, vraticemo se na stranicu index.html koja ce opet da redirektuje na stranicu user.html
            return HttpResponseRedirect(reverse("index"))
        else:                                                                  
            return render(request, "users/login.html", {                       #ako usera nema, tj ako je None, vraca nas ka login.html stranici
                "message": "Invalid credentials."                              #i prosledjuje nam ovaj recnik
            })
    else:
        return render(request, "users/login.html")                             #ako ne idemo preko forme tj ne idemo preko POST, nego ako idemo preko GET, onda nas vrati samo na login.html

def logout_view(request):                                                      #metoda za logout, koja ce nam vratiti "Logged out." kad se izlogujemo
    logout(request)                                                            #ugradjena metoda za logout
    return render(request, "users/login.html", {
        "message":"Logged out."
    })