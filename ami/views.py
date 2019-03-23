from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from .models import Barracks
from .models import GigChoice
from .models import Type
import datetime

# Create your views here.

def inspection(request):
	template = loader.get_template('ami/inspection.html')
	context = {
        'barracksList': Barracks.objects.order_by('-name')[:5],
		'gigList': GigChoice.objects.all(),
		'typeList': Type.objects.all()
	}
	return HttpResponse(template.render(context, request))

	
