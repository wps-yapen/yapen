from django.contrib import admin

from .models import Location, Pension, Room

admin.site.register(Location)
admin.site.register(Pension)
admin.site.register(Room)