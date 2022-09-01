from django.contrib import admin
from .models import Drinks
from .models import Food
from .models import Alcohol

admin.site.register(Drinks)             #registrujemo model u admin site
admin.site.register(Food)
admin.site.register(Alcohol)