from django.urls import path

from . import views

urlpatterns = [
	path('', views.overview, name='overview'),
    path('overview', views.overview, name='overview'),
    path('inspection/', views.inspection, name='inspection'),
	path('signup/', views.signup, name='signup'),
	path('settings/', views.settings, name='settings'),
]
