from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.



statuses = (
	('Pass','Pass'),
	('Fail','Fail'),
	('PMI','PMI')
)

#The Profile model is an extension of the django User model.
#The purpose is assign room, unit, and position to Users.
#This information is changed by the user on the settings page.
class Profile(models.Model):
    numUnits = (
        (1,1),
        (2,2),
        (3,3),
        (4,4)
    )
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    room = models.ForeignKey('Room',blank=True,null=True,on_delete=models.SET_NULL)
    squad = models.PositiveSmallIntegerField(choices=numUnits,blank=True,null=True)
    platoon = models.PositiveSmallIntegerField(choices=numUnits,blank=True,null=True)
    company = models.ForeignKey('Company',blank=True,null=True,on_delete=models.SET_NULL)
    position = models.ForeignKey('Position',blank=True,null=True,on_delete=models.SET_NULL)
    def __str__(self):
        return str(self.user)

#The Inspection model is used to store each individual inspection.
#Data is added from the Inspection page by users.
class Inspection(models.Model):
    statuses = (
        ('Pass','Pass'),
        ('Fail','Fail'),
        ('PMI','PMI')
    )
    date = models.DateField()
    room = models.ForeignKey('Room',blank=True,null=True,on_delete=models.SET_NULL)
    status = models.CharField(max_length=5,choices=statuses)
    choices = models.ManyToManyField('GigChoice',blank=True,null=True)
    inspector = models.ForeignKey(User,blank=True,null=True,on_delete=models.SET_NULL)
    notes = models.CharField(max_length=200,blank=True,null=True)
    def __str__(self):
        return str(str(self.date) + " - " + str(self.room))
    def gigs(self):
        num=self.choices.count()
        return(num)

#The GigChoice model is used to set what the Gigs that can be checked are.
#This can only be changed from the admin page.
class GigChoice(models.Model):
    gigName = models.CharField(max_length=100)
    gigDesc = models.CharField(max_length=300)
    type = models.ForeignKey('Type',blank=True,null=True,on_delete=models.CASCADE)
    def __str__(self):
        return str(self.gigName)

#The Position model stores what the possible positions are for cadets
#This data can only be changed from the admin page.
class Position(models.Model):
    levels = (
        ('Team','Team'),
        ('Squad','Squad'),
        ('Platoon','Platoon'),
        ('Company','Company'),
        ('Battalion','Battalion'),
        ('Regiment','Regiment'),
        ('Brigade','Brigade'),
    )
    position = models.CharField(max_length=50)
    leadershipLevel= models.CharField(max_length=50, choices = levels,blank=True,null=True)
    def __str__(self):
        return str(self.position)

#The Barracks model stores the barracks that Cadets live in.
#This data can only be changed from the admin page.
class Barracks(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return str(self.name)
    
#The Company model stores the companies that Cadets can choose.
#This data can only be changed from the admin page.        	
class Company(models.Model):
    name = models.CharField(max_length=2)
    def __str__(self):
        return str(self.name)

#The Room model stores the rooms that Cadets live in.
#Rooms are added whenever someone updates their profile with an unkown room.            
class Room(models.Model):
    number = models.PositiveSmallIntegerField()
    barracks = models.ForeignKey('Barracks',on_delete=models.CASCADE)
    def __str__(self):
        return (self.barracks.name + "-" + str(self.number))

#The Type model stores the possible gig types.
#This data can only be changed from the admin page.          
class Type(models.Model):
    name = models.CharField(max_length=100)		
    def __str__(self):
        return str(self.name)
	

#This function is used to create a profile to attach to new Users.
#It automatically runs whenever a new User is created.
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

#@receiver(post_save, sender=User)
#def save_user_profile(sender, instance, **kwargs):
#	try:
#		instance.profile.save()
#	except Exception:
#		Profile.objects.create(user=instance)
