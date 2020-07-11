from django.urls import path, include
from . import views

app_name = 'linkedin'

urlpatterns = [
    path('linkedin/', views.IndexView.as_view(), name='index'),
    path('linkedin/user/', views.ProfileView.as_view(), name='user-profile'),
]