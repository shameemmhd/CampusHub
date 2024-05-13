from django.contrib import admin
from .models import Agencys,Packages,Reservation
# Register your models here.
admin.site.register(Agencys)
admin.site.register(Packages)
admin.site.register(Reservation)