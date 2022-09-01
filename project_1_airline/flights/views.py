from django.shortcuts import render
from . models import Flight, Passenger
from django.http import HttpResponseBadRequest, HttpResponseRedirect, Http404
from django import forms
from django.urls import reverse

# Create your views here.
def index(request):                                       #metoda za 1. putanju tj path u urls.py u okviru flights foldera
    return render(request, "flights/index.html",          #indeksna stranica izlista sve flightove
    {
    "flights":Flight.objects.all()                        #zbog cega imamo ovde vracanje svih objekata
    })

def flight(request,flight_id):                             #metoda za 2. putanju tj path u urls.py u okviru flights foldera
    flight = Flight.objects.get(pk=flight_id)              #pk je primary key; on ce na osnovu tog flight_id vratiti ceo objekat i to ce biti promenljiva flight
    return render(request, "flights/flight.html",          #stranici flight.html prosledjujemo kljuc i vrednost, a vrednost je taj objekat koji smo izvukli na osnovu id
    {
    "flight":flight,                                       #objekat flight koji smo napravili iznad prosledjujemo kao vrednost kljucu
    "passengers":flight.passengers.all(),                  #putnici za taj let -> passengers vuce iz models.py red 25
    "non_passengers":Passenger.objects.exclude(flights=flight).all()        #ne-putnici, tj oni jesu putnici ali nisu prijavljeni za konkretni let koji posmatramo; dobijemo ih tako sto izvucemo objekte koji ne pripadaju ovom letu tj koji ne zadovoljavaju deo (flights=flight)
    })

def book(request, flight_id):                              #ova metoda ce dati listu putnika sa pojedinacnih letova kad udjemo na link
    if request.method == "POST":
        try:
            passenger = Passenger.objects.get(pk=int(request.POST["passenger"]))           #Passenger vadi podatak iz forme koju smo uzeli i skladisti u promenljivu passenger; element iz forme je deo ["passenger"] i mi preko njega pristupamo elementu forme i iz njega uzimamo podatke. Posto su elementi forme stringovi, radimo konverziju u int preko pk=int
            flight = Flight.objects.get(pk=flight_id)
        except KeyError:
            return HttpResponseBadRequest("Bad Request: no flight chosen")
        except Flight.DoesNotExist:
            return HttpResponseBadRequest("Bad Request: flight does not exist")
        except Passenger.DoesNotExist:
            return HttpResponseBadRequest("Bad Request: passenger does not exist")
        passenger.flights.add(flight)                                                      #u letove za tog putnika dodajemo taj let
        return HttpResponseRedirect(reverse("flight", args=(flight_id,)))                  #vratice putanju koja ce u sebi imati flight, a argument te putanje ce biti flight_id