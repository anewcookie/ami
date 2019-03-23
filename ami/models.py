from django.db import models

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

class Cadet(models.Model):
	firstName = models.CharField(max_length=50)
	lastName = models.CharField(max_length=50)
	xnumber = models.PositiveSmallIntegerField(primary_key = True)
	room = models.PositiveSmallIntegerField()
	barracks = models.ForeignKey('Barracks',null=True,on_delete=models.SET_NULL)
	squad = models.PositiveSmallIntegerField(choices=numUnits)
	platoon = models.PositiveSmallIntegerField(choices=numUnits)
	company = models.ForeignKey('Company',null=True,on_delete=models.SET_NULL)
	position = models.ForeignKey('Position',null=True,on_delete=models.SET_NULL)
	
class Inspection(models.Model):
	#ID (AutoField) is implied
	date = models.DateField()
	room = models.PositiveSmallIntegerField()
	barracks = models.ForeignKey('Barracks',null=True,on_delete=models.SET_NULL)
	status = models.CharField(max_length=5,choices=statuses) 
	inspector = models.ForeignKey('Cadet',null=True,on_delete=models.SET_NULL)
	notes = models.CharField(max_length=200)

class GigChoice(models.Model):
	gig = models.CharField(max_length=300, primary_key = True)
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