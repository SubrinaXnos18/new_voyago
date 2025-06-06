from django.contrib import admin
from .models import Package, Booking, Diary, Contact

admin.site.register(Package)
admin.site.register(Booking)
admin.site.register(Diary)
admin.site.register(Contact)
