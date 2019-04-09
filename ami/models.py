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
        
class GigChoice(models.Model):
    gigName = models.CharField(max_length=100)
    gigDesc = models.CharField(max_length=300)
    type = models.ForeignKey('Type',blank=True,null=True,on_delete=models.CASCADE)
    def __str__(self):
        return str(self.gigName)
    
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
        	
class Barracks(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return str(self.name)
        	
class Company(models.Model):
    name = models.CharField(max_length=2)
    def __str__(self):
        return str(self.name)
        
class Room(models.Model):
    number = models.PositiveSmallIntegerField()
    barracks = models.ForeignKey('Barracks',on_delete=models.CASCADE)
    def __str__(self):
        return (self.barracks.name + "-" + str(self.number))
        
class Type(models.Model):
    name = models.CharField(max_length=100)		
    def __str__(self):
        return str(self.name)
	

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