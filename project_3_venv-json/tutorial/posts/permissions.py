from rest_framework import permissions                          #permissions se uzima iz rest_framework API

#ovaj fajl radi proveru autentikacije
class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permissions(self, request, view, obj):       
        if request.method in permissions.SAFE_METHODS:          #vratice nesto ako je zahtevana metoda u grupi sigurnih metoda
            return True
        return obj.owner == request.user                        #ili ako se poklapa owner i requester (vlasnik je onaj koji trazi pristup toj metodi)