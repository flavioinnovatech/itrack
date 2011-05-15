from django.forms import ModelForm, TextInput
from itrack.accounts.models import UserProfile
from django.contrib.auth.models import User

class UserProfileForm(ModelForm):
	    class Meta:
	        model = UserProfile
	        exclude = ('user')

class UserForm(ModelForm):
    class Meta:
            model = User
            exclude = ('is_staff', 'is_active', 'is_superuser', 'last_login', 'date_joined')
            #exclude = ('title','system')
            
