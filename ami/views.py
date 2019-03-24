from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.db import transaction
from django.contrib import messages

from .models import Barracks
from .models import GigChoice
from .forms import *
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

@login_required
@transaction.atomic
def settings(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('/')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'ami/settings.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


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
    return render(request, 'ami/signup.html', {'form': form})
	
