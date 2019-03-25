from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

numUnits = (
	(1,1),
	(2,2),
	(3,3),
	(4,4)
)

levels = (
	('Team','Team'),
	('Squad','Squad'),
	('Platoon','Platoon'),
	('Company','Company'),
	('Battalion','Battalion'),
	('Regiment','Regiment'),
	('Brigade','Brigade'),
)

statuses = (
	('Pass','Pass'),
	('Fail','Fail'),
	('PMI','PMI')
)

class Profile(models.Model):
	user = models.OneToOneField(User,on_delete=models.CASCADE,primary_key = True)
	room = models.PositiveSmallIntegerField(null=True)
	barracks = models.ForeignKey('Barracks',null=True,on_delete=models.SET_NULL)
	squad = models.PositiveSmallIntegerField(choices=numUnits,null=True)
	platoon = models.PositiveSmallIntegerField(choices=numUnits,null=True)
	company = models.ForeignKey('Company',null=True,on_delete=models.SET_NULL)
	position = models.ForeignKey('Position',null=True,on_delete=models.SET_NULL)
	
class Inspection(models.Model):
	#ID (AutoField) is implied
	date = models.DateField()
	room = models.PositiveSmallIntegerField()
	barracks = models.ForeignKey('Barracks',null=True,on_delete=models.SET_NULL)
	status = models.CharField(max_length=5,choices=statuses)
	gigs = models.IntegerField()
	inspector = models.ForeignKey(User,null=True,on_delete=models.SET_NULL)
	notes = models.CharField(max_length=200,null=True)

class GigChoice(models.Model):
	gigName = models.CharField(max_length=100, primary_key = True)
	gigDesc = models.CharField(max_length=300)
	type = models.ForeignKey('Type',null=True,on_delete=models.CASCADE)

class Position(models.Model):
	position = models.CharField(max_length=50, primary_key = True)
	leadershipLevel= models.CharField(max_length=50, choices = levels)
	
class Barracks(models.Model):
	name = models.CharField(max_length=50, primary_key = True)
	
class Checklist(models.Model):
	#ID (AutoField) is implied
	inspectionID = models.ForeignKey('Inspection',on_delete=models.CASCADE)
	gig = models.ForeignKey('GigChoice',null=True,on_delete=models.SET_NULL)
	
class Company(models.Model):
	name = models.CharField(max_length=2, primary_key = True)

class Type(models.Model):
	name = models.CharField(max_length=100, primary_key = True)		
	

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
	try:
		instance.profile.save()
	except Exception:
		Profile.objects.create(user=instance)