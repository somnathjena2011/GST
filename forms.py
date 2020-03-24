from django import forms
from django.contrib.auth.forms import AuthenticationForm, UsernameField
from .models import User, TaxpayerProfile, OfficialProfile
from .backends import TaxpayerBackend, OfficialBackend
import re
class UserForm(forms.ModelForm):
	first_name = forms.CharField(max_length=200)
	last_name = forms.CharField(max_length=200)
	email = forms.EmailField()
	password = forms.CharField(widget=forms.PasswordInput)
	class Meta:
		model = User
		fields = ['first_name', 'last_name', 'email', 'password']
		widgets = {
			'password': forms.PasswordInput(attrs={'class':'inp'}),
			'first_name': forms.TextInput(attrs={'class':'inp'}),
			'last_name': forms.TextInput(attrs={'class':'inp'}),
			'email': forms.EmailInput(attrs={'class': 'inp'}),
			'aadhar': forms.TextInput(attrs={'class':'inp'})
		}
	#def clean_name(self, *args, **kwargs):
	#	name = self.data['name']
	#	for c in name:
	#		if (not c.isalpha()) or (not c==' '):
	#			raise forms.ValidationError("Enter a valid name\n")
	#	print(name)
	#	return name
	#def clean_password(self, *args, **kwargs):
	#	password = self.data['password']
	#	if len(password)<8 : 
	#		raise forms.ValidationError('Too short password\n')
	#	print(password)
	#	return password
	#def clean_email(self, *args, **kwargs):
	#	email = self.data['email']
	#	regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
	#	if not re.search(regex,email):
	#		raise forms.ValidationError('Not valid email')
	#	else:
	#		print(email)
	#		return email

class TaxpayerProfileForm(forms.ModelForm):
	class Meta:
		model = TaxpayerProfile
		fields = ['aadhar']

class OfficialProfileForm(forms.ModelForm):
	class Meta:
		model = OfficialProfile
		fields = ['aadhar', 'uid']

class TaxpayerLoginForm(forms.ModelForm):
	email = forms.EmailField()
	password = forms.CharField(widget=forms.PasswordInput)
	class Meta:
		model=User
		fields = ['email', 'password']
		widgets = {
			'email': forms.EmailInput(attrs={'class': 'inp'}),
			'password': forms.PasswordInput(attrs={'class':'inp'})
		}
	#email = EmailField(
	#		label='Email',
	#		widget=forms.EmailInput()
	#	)

class OfficialLoginForm(forms.ModelForm):
	email = forms.EmailField()
	password = forms.CharField(widget=forms.PasswordInput)
	class Meta:
		model=User
		fields = ['email', 'password']
		widgets = {
			'email': forms.EmailInput(attrs={'class': 'inp'}),
			'password': forms.PasswordInput(attrs={'class':'inp'})
		}
	#email = EmailField(
	#		label='Email',
	#		widget=forms.TextInput()
	#	)