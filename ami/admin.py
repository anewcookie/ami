from django.contrib import admin

# Register your models here.

from .models import *


admin.site.register(Profile)
admin.site.register(Inspection)
admin.site.register(Barracks)
admin.site.register(Position)
admin.site.register(GigChoice)
admin.site.register(Company)
admin.site.register(Type)
admin.site.register(Room)