from django.contrib import admin
from .models import Agencys,Packages,Reservation,UserProfile,Calendar
# Register your models here.
admin.site.register(Agencys)
admin.site.register(Packages)
admin.site.register(Reservation)
admin.site.register(UserProfile)
admin.site.register(Calendar)