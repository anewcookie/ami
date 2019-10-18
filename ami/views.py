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

#The overview view shows a background picture.
#This is the home/landing page for the website.
def overview(request):
    template = loader.get_template('ami/overview.html')
    context = {
        'test': 'test'
       }
    return HttpResponse(template.render(context, request))	

#The summary page shows the status of rooms by company.
def summary(request,company):
    template = loader.get_template('ami/summary.html')
    if company=="0":
        try:
            company=request.user.profile.company.name
        except Exception:
            company="A1"
    profileList=Profile.objects.filter(company__name=company).order_by('room')
    roomList=set()
    passCount = 0
    failCount = 0
    pmiCount = 0
    nullCount = 0
    for profile in profileList:
        roomList.add(profile.room)
    for room in roomList:
        room.occupants=Profile.objects.filter(room=room)
        print(room.occupants)
        inspection = Inspection.objects.filter(date=datetime.datetime.now().date(),room=room)
        if inspection:
            status=inspection[0].status
            room.status=status
            if status == "Pass":
                passCount += 1
            elif status == "Fail":
                failCount += 1
            elif status == "PMI":
                pmiCount += 1		
        else:
            room.status=None
            nullCount += 1

    context = {
        'companyList': Company.objects.order_by('name'),
        'home':company,
        'roomList': roomList,
	'passCount': passCount,
	'failCount': failCount,
	'pmiCount' : pmiCount,
	'nullCount' : nullCount,
       }
    return HttpResponse(template.render(context, request))	    


#The inspection page allows users to inspect rooms. 
@login_required
def inspection(request):
    if request.method == 'POST':
        form = request.POST
        print(form)
        date = datetime.datetime.now().date()
        room = Room.objects.get(barracks__name=form['barracks'], number=form['room'])
        status = form['finalStatus']
        inspector = request.user
        notes = form['notes']
        i = Inspection(date=date,room=room,status=status,inspector=inspector,notes=notes)
        i.save() 
        for key in form:
            if form[key] == "on":
                inspectionID = i
                gig = GigChoice.objects.get(gigName=key)
                i.choices.add(gig)
        
        i.save()        

        
        
        messages.success(request, 'Inspection submitted successfully!')
        return redirect('/')

    template = loader.get_template('ami/inspection.html')
    try:
        home = request.user.profile.room.barracks.name
    except Exception:
        messages.error(request, 'Please update your barracks information.')
        return redirect('/settings/')
    context = {
        'title':"My Room",
        'barracksList': Barracks.objects.order_by('name'),
        'gigList': GigChoice.objects.all(),
        'typeList': Type.objects.all(),
        'home':home,
       }
    return HttpResponse(template.render(context, request))	

#The myRoom page shows the history of a room.
@login_required
def myRoom(request,room):
    template = loader.get_template('ami/room.html')
    if room == "myroom":
        try:
            room = str(request.user.profile.room)
        except Exception:
            messages.error(request, 'Please update your barracks and room information.')
            return redirect('/settings/')
        
    context = {
        'inspectionList': Inspection.objects.filter(room__barracks__name=room.split("-")[0],room__number=int(room.split("-")[1])).order_by("-date"),
        'room':room,
       }
    return HttpResponse(template.render(context, request))	

#This view has not been set, but is here for future website development.
#The idea behind this view was to show a User his subordinates' room status and history.
@login_required
def subordinates(request):
	pass

#The settings view is used to change a user's User, Room, and Profile information
@login_required
@transaction.atomic
def settings(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        room_form = RoomForm(request.POST)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid() and room_form.is_valid():
            user_form.save()
            profile_form.save()
            newRoom = Room.objects.get_or_create(number=room_form.cleaned_data['number'],barracks=room_form.cleaned_data['barracks'])
            request.user.profile.room = newRoom[0]
            request.user.profile.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('/')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        user_form = UserForm(instance=request.user)
        if request.user.profile.room:
            roomInfo = request.user.profile.room.number
            room_form = RoomForm(initial={'number': request.user.profile.room.number, 'barracks': request.user.profile.room.barracks})
        else:
            room_form = RoomForm()
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'ami/settings.html', {
        'user_form': user_form,
        'room_form': room_form,
        'profile_form': profile_form
    })

#The signup page allows new users to sign up for accounts.
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
	
