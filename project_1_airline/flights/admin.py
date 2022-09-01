from django.contrib import admin
from . models import Flight,Airport, Passenger             #mora tacka ispred models da se doda da program zna da to nije neki nas models modul vec neki ugradjeni

#Register your models here.
#donje 2 klase smo dodali kako bi imali u Passengers delu kad se klikne na putnika 2 tabele gde se odabere let klikom, dok smo za Flights promenili samo listu kako prikaze tj ne vidi se razlika
class FlightAdmin(admin.ModelAdmin):
    list_display = ("__str__", "duration")

class PassengerAdmin(admin.ModelAdmin):
    filter_horizontal = ("flights",)

admin.site.register(Airport)                               #ubacujemo na admin sajt Airport tabelu
admin.site.register(Flight, FlightAdmin)                   #ubacujemo na admin sajt Flight tabelu
admin.site.register(Passenger, PassengerAdmin)             #ubacujemo na admin sajt Passenger tabelu