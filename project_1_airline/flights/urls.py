from django.urls import path
from.import views


urlpatterns = [
    path("", views.index, name="index"),
    path("<int:flight_id>",views.flight,name="flight"),        #"<int:flight_id> znaci da kad posle kose crte u URL napisemo neki broj, on pokrene ovaj path
                                                               #znaci kad u URL unesemo /flights, izbacice listu svih letova, a kad nastavimo sa nekim brojem npr /flight/2 izbacice podatke leta sa id=2
    path("<int:flight_id>/book",views.book,name="book")
]                                                              