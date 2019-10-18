from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile
from .models import Room
from django.core.exceptions import ValidationError

def validate_email(value):
    if '@westpoint.edu' not in value:
        raise ValidationError('Please enter a valid westpoint.edu address')

#This form is shown to users who want to create a new account.
class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=254, help_text='Input a valid westpoint.edu address.', validators=[validate_email])
	
	
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )

#This form is shown on the settings page and allows users to change their User information.	
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
        
#This form is shown on the settings page and allows users to change their Room information.	
class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ('number', 'barracks')
        
#This form is shown on the settings page and allows users to change their Profile information.	    
class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ('squad', 'platoon', 'company') #took out positions until I can make it secure
