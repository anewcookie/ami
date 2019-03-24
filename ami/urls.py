from django.urls import path

from . import views

urlpatterns = [
	path('', views.inspection, name='inspection'),
    path('inspection/', views.inspection, name='inspection'),
	path('signup/', views.signup, name='signup'),
	path('settings/', views.settings, name='settings'),
]
