from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'accounts'

urlpatterns = [
    path('taxpayer/registration',views.taxpayer_profile_view,name='taxpayer'),
    path('official/registration',views.official_profile_view,name='official'),
    path('taxpayer/login',views.taxpayer_login,name='taxpayer_login'),
    path('official/login',views.official_login,name='official_login'),
]