from django.contrib import admin

# Register your models here.

from .models import Profile
from .models import Inspection
from .models import Barracks
from .models import Position
from .models import Checklist
from .models import GigChoice
from .models import Company
from .models import Type
from .models import Room

admin.site.register(Profile)
admin.site.register(Inspection)
admin.site.register(Barracks)
admin.site.register(Position)
admin.site.register(Checklist)
admin.site.register(GigChoice)
admin.site.register(Company)
admin.site.register(Type)
admin.site.register(Room)