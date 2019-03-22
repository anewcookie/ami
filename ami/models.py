from django.db import models

# Create your models here.

1to4 = (
	(1,1),
	(2,2),
	(3,3),
	(4,4)
)

levels = (
	('Team'),
	('Squad'),
	('Platoon'),
	('Company'),
	('Battalion'),
	('Regiment'),
	('Brigade'),
)

statuses = (
	('Pass','Pass'),
	('Fail','Fail'),
	('PMI','PMI')
)

class Cadet(models.Model):
    firstName = models.CharField(max_length=50)
	lastName = models.CharField(max_length=50)
    xnumber = models.PositiveSmallIntegerField(max_length=5,min_length=5, primary_key = True)
    room = models.PositiveSmallIntegerField(max_length=5)
	barracks = models.ForeignKey('Barracks',null=True,on_delete=models.SET_NULL)
	squad = models.PositiveSmallIntegerField(max_length=1,choices=1to4)
	platoon = models.PositiveSmallIntegerField(max_length=1,choices=1to4)
	company = models.ForeignKey('Company',null=True,on_delete=models.SET_NULL)
	position = models.ForeignKey('Position',null=True,on_delete=models.SET_NULL)
	
class Inspection(models.Model):
	#ID (AutoField) is implied
    date = models.DateField()
	room = models.PositiveSmallIntegerField(max_length=5)
	barracks = models.ForeignKey('Barracks',null=True,on_delete=models.SET_NULL)
	status = models.CharField(max_length=5,choices=statuses) 
	inspector = models.ForeignKey('Cadet',null=True,on_delete=models.SET_NULL)
	notes = models.CharField(max_length=200)

class Gig(models.Model):
    gig = models.CharField(max_length=200, primary_key = True)
	autoFailure = models.BooleanField()

class Position(models.Model):
    position = models.CharField(max_length=50, primary_key = True)
	leadershipLevel= models.CharField(max_length=50, choices = levels)
	
class Barracks(models.Model):
    name = models.CharField(max_length=50, primary_key = True)
	
class Checklist(models.Model):
	#ID (AutoField) is implied
    inspectionID = models.ForeignKey('Inspection',on_delete=models.CASCADE)
	gig = models.ForeignKey('Gig',null=True,on_delete=models.SET_NULL)
	
class Company(models.Model):
	name = models.CharField(max_length=2, primary_key = True)	