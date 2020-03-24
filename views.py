from django.contrib.auth import login, authenticate
from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import CreateView
from .forms import OfficialProfileForm, TaxpayerProfileForm, UserForm, TaxpayerLoginForm, OfficialLoginForm
from django.contrib.auth.forms import AuthenticationForm
from .models import User, TaxpayerProfile, OfficialProfile
from .backends import TaxpayerBackend, OfficialBackend

def taxpayer_profile_view(request):
	if request.method == 'POST':
		print("22222")
		user_form = UserForm(request.POST)
		taxpayer_profile_form = TaxpayerProfileForm(request.POST)
		#print(user_form.data['name'])
		if user_form.is_valid() is not None:
			print("yesssssssssss")
			user=User()
			user.first_name=user_form.data['first_name']
			user.last_name=user_form.data['last_name']
			#user.username=user.first_name+user.last_name
			user.email=user_form.data['email']
			user.password=user_form.data['password']
			user.is_taxpayer=True
			tax=TaxpayerProfile()
			tax.user=user
			tax.aadhar=taxpayer_profile_form.data['aadhar']
			user.gstin=tax.aadhar+user.first_name[0:2]
			#user.username=user.email
			print(user.gstin)
			if len(str(tax.aadhar))!=12:
				return HttpResponse('AADHAR must be 12 digit')
			else: 
				try:
					ob1=TaxpayerProfile.objects.get(aadhar=tax.aadhar) 
					ob2=User.objects.get(gstin=user.gstin)
					ob3=User.objects.get(email=user.email)
					return HttpResponse('User exists') 
				except (User.DoesNotExist,TaxpayerProfile.DoesNotExist):
					user.save()
					print(user.id)
					print(tax.user.id)
					tax.user=user
					tax.save()
					#user.save()
					print(user.email)
					return HttpResponse('thanks')

		else:
			print("noooooooooo")
			user_form = UserForm()
			taxpayer_profile_form = TaxpayerProfileForm()
			return render(request, 'accounts/taxpayer_profile.html', {'user_form':user_form, 'taxpayer_profile_form':taxpayer_profile_form})

	else:
		#print("1111")
		user_form = UserForm()
		taxpayer_profile_form = TaxpayerProfileForm()
		return render(request, 'accounts/taxpayer_profile.html', {'user_form':user_form, 'taxpayer_profile_form':taxpayer_profile_form})


def official_profile_view(request):
	if request.method == 'POST':
		#print("22222")
		user_form = UserForm(request.POST)
		official_profile_form = OfficialProfileForm(request.POST)
		if user_form.is_valid() is not None :

			#print("yesssssssssss")
			user=User()
			user.first_name=user_form.data['first_name']
			user.last_name=user_form.data['last_name']
			#user.username=user.first_name+user.last_name
			user.email=user_form.data['email']
			user.password=user_form.data['password']
			user.is_official=True
			official=OfficialProfile()
			official.user=user
			official.aadhar=official_profile_form.data['aadhar']
			official.uid=official_profile_form.data['uid']
			user.gstin=official.aadhar+user.first_name[0:2]
			#user.username=user.email
			if len(str(official.aadhar))!=12:
				return HttpResponse('AADHAR must be 12 digit')
			else: 
				try:
					ob1=OfficialProfile.objects.get(aadhar=official.aadhar) 
					ob2=User.objects.get(gstin=user.gstin)
					ob3=User.objects.get(email=user.email)
					ob4=OfficialProfile.objects.get(uid=official.uid)
					return HttpResponse('User exists') 
				except (User.DoesNotExist,OfficialProfile.DoesNotExist):
					user.save()
					official.user=user
					official.save()
					print(user.email)
					return HttpResponse('thanks')


		else:
			#print("noooooooooo")
			user_form = UserForm()
			official_profile_form = OfficialProfileForm()
			return render(request, 'accounts/official_profile.html', {'user_form':user_form, 'official_profile_form':official_profile_form})

	else:
		#print("1111")
		user_form = UserForm()
		official_profile_form = OfficialProfileForm()
		return render(request, 'accounts/official_profile.html', {'user_form':user_form, 'official_profile_form':official_profile_form})

def taxpayer_login(request):
	if request.method == 'POST':
		print("yes")
		form = TaxpayerLoginForm(request.POST)
		if form.is_valid() is not None:
			print("yes2")
			#user = form.get_user()
			user=User()
			email=form.data['email']
			password=form.data['password']
			try:
				ob1=User.objects.get(email=email)
				if ob1.password == password and ob1.is_taxpayer is True:
					print("yes3")
					#ob2=TaxpayerProfile.objects.get(password=user.password)
					#ob=TaxpayerBackend.authenticate(email=email,password=password)
					login(request, ob1, backend='accounts.backends.TaxpayerBackend')
					return HttpResponse("Logged in")
				else:
					return HttpResponse("No such user")
			except (TaxpayerProfile.DoesNotExist):
				return HttpResponse("No such user")
	else:
		print("no")
		form=TaxpayerLoginForm()
	return render(request,"accounts/taxpayer_login.html",{'form':form})

def official_login(request):
	if request.method == 'POST':
		print("yes")
		form = OfficialLoginForm(request.POST)
		if form.is_valid() is not None:
			print("yes2")
			#user = form.get_user()
			user=User()
			email=form.data['email']
			password=form.data['password']
			try:
				ob1=User.objects.get(email=user.email)
				if ob1.password == password and ob1.is_official is True:
					print("yes3")
					#ob2=TaxpayerProfile.objects.get(password=user.password)
					login(request, ob1, backend='accounts.backends.OfficialBackend')
					return HttpResponse("Logged in")
				else:
					return HttpResponse("No such user")
			except (OfficialProfile.DoesNotExist):
				return HttpResponse("No such user")
	else:
		print("no")
		form=OfficialLoginForm()
	return render(request,"accounts/official_login.html",{'form':form})

#def official_login(request):
#	if request.method == 'POST':
#		form = OfficialLoginForm(data=request.POST)
#		if form.is_valid() is not None:
#			user = form.get_user()
#			login(request, user)
#			return HttpResponse("Logged in")
#	else:
#		form=OfficialLoginForm()
#	return render(request,"accounts/official_login.html",{'form':form})