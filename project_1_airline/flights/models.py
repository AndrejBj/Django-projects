from django.db import models

import flights

# Create your models here.
class Airport(models.Model):                                         #napravili smo klasu Airport koja je izvucena iz vec postojece klase Model u okviru models modula
    code = models.CharField(max_length=3)                            #Charfield je string field, gde ubacujemo string
    city = models.CharField(max_length=64)
 
    def __str__(self):
        return f"{self.city} ({self.code})"


class Flight(models.Model):                                          #napravili smo klasu Flight koja je izvucena iz vec postojece klase Model u okviru models modula
    origin = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="departures")          #cascade znaci da ako promenimo ili obrisemo roditeljsku tabelu, automatski menjamo/brisemo i decju (referencijalni integritet)
    destination = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="arrivals")
    duration = models.IntegerField()                                 #Integerfield je integer field, gde ubacujemo brojeve

    def __str__(self):
        return f"{self.id} : {self.origin} to {self.destination}"    #metod koji smo ubacili u klasu preko koje cemo ubacivati stringove

    def is_valid_flight(self):
        return self.origin != self.destination and self.duration >= 0    #ovaj metod smo dodali u okviru testiranja; testiramo da polaziste i destinacija ne mogu da budu isti i let da traje sigurno duze od 0

class Passenger(models.Model):
    first = models.CharField(max_length=64)                          #ime koje unosimo sa max 64 slova
    last = models.CharField(max_length=64)                           #prezime koje unosimo sa max 64 slova
    flights = models.ManyToManyField(Flight,blank=True,related_name="passengers")              #ManyToManyField je polje koje je u sql vezano za vise prema vise relaciju, s obzirom da vise putnika moze da rezervise vise letova
                                                                                               #ovde pravimo vezu izmedju klasa Passenger i Flight, blank je za putnike koji nemaju rezervisan let, related_name deo omogucava da moze iz letova da se pristupi putnicima (znaci moze onda u oba pravca)
#u prevodu, preko promenljive flighs, mi za klasu Passenger dolazimo do letova, dok smo u delu related_name="passengers" omogucili i obrnuto, da iz Flight klase vidimo koji se putnici nalaze na letu

    def __str__(self):
        return f"{self.first} {self.last}"                           #to string za putnika, u redovima 23 i 24 smo definisali first i last; gore smo u to string imali dvotacku, ali ovde smo je izbacili da ne izbacuje ime:prezime
