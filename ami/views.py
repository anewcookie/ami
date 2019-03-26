from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.db import transaction
from django.contrib import messages

from .models import *
from .forms import *
from .models import Type
import datetime

# Create your views here.

def overview(request):
    template = loader.get_template('ami/overview.html')
    context = {
        'test': 'test'
       }
    return HttpResponse(template.render(context, request))	

@login_required
def inspection(request):
    if request.method == 'POST':
        form = request.POST
        print(form)
        date = datetime.datetime.now().date()
        room = form['room']
        barracks = Barracks(form['barracks'])
        status = form['finalStatus']
        gigs = form['gigNumber']
        inspector = request.user
        notes = form['notes']
        i = Inspection(date=date,room=room,barracks=barracks,status=status,gigs=gigs,inspector=inspector,notes=notes)
        i.save()
        
        for key in form:
            if form[key] == "on":
                inspectionID = i
                gig = GigChoice(key)
                c = Checklist(inspectionID=inspectionID,gig=gig)
                c.save()
        
        
        messages.success(request, 'Inspection submitted successfully!')
        return redirect('/')

    template = loader.get_template('ami/inspection.html')
    try:
        home = request.user.profile.barracks.name
    except Exception:
        messages.error(request, 'Please update your barracks information.')
        return redirect('/settings/')
    context = {
        'barracksList': Barracks.objects.order_by('name'),
        'gigList': GigChoice.objects.all(),
        'typeList': Type.objects.all(),
        'home':home,
       }
    return HttpResponse(template.render(context, request))	
	
@login_required
def myRoom(request):
    template = loader.get_template('ami/room.html')
    
    inspections = Inspection.objects.filter(room=request.user.profile.room).order_by("-date")
    inspectionList = []
    for inspection in inspections:
        inspection.gigsData = Checklist.objects.filter(inspectionID=inspection.id)
        inspectionList.append(inspection)
    print(inspectionList)
        
    context = {
        'inspectionList': inspectionList,
       }
    return HttpResponse(template.render(context, request))	

	
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
	
