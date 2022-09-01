from django.test import TestCase        #ne moramo da importujemo unittest, posto je django.test vec biblioteka koja se time bavi

# Create your tests here.

from django.db.models import Max
from django.test import Client, TestCase                                        #Client je objekat koji upucuje akcije ka browseru

from .models import Airport, Flight, Passenger

# Create your tests here.
class FlightTestCase(TestCase):                                                 #TestCase je pokupljen iz djangovog framework-a, ne treba da unittest.TestCase kao sa unittest importom

    def setUp(self):                                                            #setUp() se poziva pre samog testiranja ostalih metoda; ona kreira okruzenje za testiranje
 
        # Create airports.
        a1 = Airport.objects.create(code="AAA", city="City A")                  #za testiranje nam nije potrebna cela baza, vec napravimo model koji cemo da testiramo, u ovom slucaju napravili smo 2 aerodroma i 3 leta
        a2 = Airport.objects.create(code="BBB", city="City B")                  #(kao npr sto smo kod masinskog ucenja zakljucke po osnovu trenaznih podataka testirali na testnim podacima, tako ovde bazu testiramo na osnovu modela)

        # Create flights.
        Flight.objects.create(origin=a1, destination=a2, duration=100)          #simuliramo normalan let
        Flight.objects.create(origin=a1, destination=a1, duration=200)          #simuliramo gresku - let sa istim polazistem i destinacijom
        Flight.objects.create(origin=a1, destination=a2, duration=-100)         #simuliramo gresku - let sa negativnim vremenom

    def test_departures_count(self):                                            #metode koje testiramo pocinju sa test
        a = Airport.objects.get(code="AAA")                                     #1. test - da li imamo 3 polaska sa prvo aerodroma? da
        self.assertEqual(a.departures.count(), 3)                               #a.departures.count() je vrednost koja se dogodila, 3 je vrednost koju ocekujemo

    def test_arrivals_count(self):
        a = Airport.objects.get(code="AAA")                                     #2. test - da li imamo 1 dolazak na prvi aerodrom? da
        self.assertEqual(a.arrivals.count(), 1)

    def test_valid_flight(self):
        a1 = Airport.objects.get(code="AAA")                                    #3. test - da li je validan let? 
        a2 = Airport.objects.get(code="BBB")
        f = Flight.objects.get(origin=a1, destination=a2, duration=100)
        self.assertTrue(f.is_valid_flight())                                    #pozivamo is_valid_flight iz models.py, koja kaze da bi let bio validan, trebaju polaziste i destinacija biti razliciti i vreme leta pozitivno; ocekujemo True, ako je suprotno test pada

    def test_invalid_flight_destination(self):                                  #4. test - da li je polaziste razlicito od dolaska?
        a1 = Airport.objects.get(code="AAA")
        f = Flight.objects.get(origin=a1, destination=a1)
        self.assertFalse(f.is_valid_flight())                                   #ocekujemo False, ako je suprotno test pada

    def test_invalid_flight_duration(self):                                     #5. test - da li je nevalidan let? 
        a1 = Airport.objects.get(code="AAA")
        a2 = Airport.objects.get(code="BBB")
        f = Flight.objects.get(origin=a1, destination=a2, duration=-100)  
        self.assertFalse(f.is_valid_flight())                                   #ako je lose postavljena metoda is_valid_flight npr da je "or" umesto "and" onda bi ovo proslo, pa bi nama bilo True iako ocekujemo False, pa bi test pao

    def test_index(self):                                                       #6. test - da li se vraca tacna web stranica koju ukucamo u url?  
        c = Client()                                                            #Client je objekat koji smo importovali koji ukucava umesto nas putanje u url (inace bi morali mi rucno to da radimo)
        response = c.get("/flights/")                                           #response kad ukucamo /flights/ u url, da li radi
        print(response)                                                         #ovo mozemo i zakomentarisati, ispise <HttpResponse status_code=200, "text/html; charset=utf-8"> gde vidimo da je status kod 200
        self.assertEqual(response.status_code, 200)                             #response.status_code se odnosi na statusni kod koji se vraca prilikom ucitavanja stranice, gde je 200 za uspesno ucitavanje, 404 jer error itd
        self.assertEqual(response.context["flights"].count(), 3)                #da li je broj letova 3? U ovaj model koji testira stavili smo 3 leta, pa da li vraca 3

    def test_valid_flight_page(self):                                           #7. test - da li vraca dobar id leta?
        a1 = Airport.objects.get(code="AAA")
        f = Flight.objects.get(origin=a1, destination=a1)                       #iz reda 21 vidimo da origin=a1, destination=a1 ima id=2 (python sam prepozna po default jer je drugi po redu), ali ga mi dole ne ukucavamo vec samo saljemo id

        c = Client()
        response = c.get(f"/flights/{f.id}")                                    #npr /flights/1, /flights/2, /flights/3;
        self.assertEqual(response.status_code, 200)

    def test_invalid_flight_page(self):                                         #8. test - testiramo max id, tj ako bi u ovom primeru povecali max id za 1, to bi bilo 4
        max_id = Flight.objects.all().aggregate(Max("id"))["id__max"]           #objects.all() vraca sve objekte za letove, aggregate() izdvaja let sa max id i sa ["id__max"] vraca taj id

        c = Client()
        response = c.get(f"/flights/{max_id + 1}")
        self.assertEqual(response.status_code, 404)                             #i broj 4 bi trebalo da vrati kao error 404 jer ne postoji

    def test_flight_page_passengers(self):                                      #9. test - da li su svi putnici ubaceni po letu
        f = Flight.objects.get(pk=1)                                            #na let 1
        p = Passenger.objects.create(first="Alice", last="Adams")               #smo kreirali 2 putnika
        f.passengers.add(p)                                                     #i dodali ih u avion

        c = Client()
        response = c.get(f"/flights/{f.id}")                                    #testiramo da li ce se vratiti stranica
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["passengers"].count(), 1)             #context je ugradjeni objekat koji vraca sve sto zahtevamo od njega (radi kao recnik); context["passengers"] vraca vrednost putnika (key je valjda context), count broj tih vrednosti; 1 ocekujemo da cemo dobiti

    def test_flight_page_non_passengers(self):                                  #10. test - da li prepozna putnike koji ne bi trebalo da budu na letu
        f = Flight.objects.get(pk=1)
        p = Passenger.objects.create(first="Alice", last="Adams")

        c = Client()
        response = c.get(f"/flights/{f.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["non_passengers"].count(), 1)         #svakog kreiranog putnika koji nije putnik konkretnog leta stavljamo u non-passengers; ocekujemo da cemo dobiti 1

#poslednje 3 funkcije padaju test, ne znam zasto, mozda sql (probao ali ne radi i dalje)