from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect

from .models import Barracks
from .models import GigChoice
from .forms import SignUpForm
from .models import Type
import datetime

# Create your views here.

def overview(request):
	pass

def inspection(request):
	template = loader.get_template('ami/inspection.html')
	context = {
        'barracksList': Barracks.objects.order_by('-name')[:5],
		'gigList': GigChoice.objects.all(),
		'typeList': Type.objects.all()
	}
	return HttpResponse(template.render(context, request))	
	
@login_required
def myRoom(request):
	pass

	
@login_required
def subordinates(request):
	pass

def settings(request):
	pass


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('settings')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})
	
