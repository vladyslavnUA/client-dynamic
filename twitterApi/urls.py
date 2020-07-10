from django.urls import path, include
from . import views

app_name = 'twitter'

urlpatterns = [
    path('twitter/user/', views.ProfileView.as_view(), name='user-profile'),
]