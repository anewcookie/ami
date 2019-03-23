from django.contrib import admin

# Register your models here.

from .models import Cadet
from .models import Inspection
from .models import Barracks
from .models import Position
#from .models import Checklist
from .models import GigChoice
from .models import Company
from .models import Type

admin.site.register(Cadet)
admin.site.register(Inspection)
admin.site.register(Barracks)
admin.site.register(Position)
#admin.site.register(Checklist)
admin.site.register(GigChoice)
admin.site.register(Company)
admin.site.register(Type)