from django.urls import path
from . import views

app_name = 'clients'

urlpatterns = [
    path('', views.IndexView.as_view(), name='dashboard'),
    path('user/', views.UserProfileView.as_view(), name='user-profile'),
    
]