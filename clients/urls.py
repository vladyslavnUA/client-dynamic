from django.urls import path
from . import views

app_name = 'clients'

urlpatterns = [
    path('', views.IndexView.as_view(), name='home'),
]