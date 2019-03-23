from django.urls import path

from . import views

urlpatterns = [
    path('inspection', views.inspection, name='inspection'),
]
