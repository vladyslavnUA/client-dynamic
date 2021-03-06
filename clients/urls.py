from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

app_name = 'clients'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('clientele/', views.ClienteleView.as_view(), name='clientele'),
    path('clientele/new', views.ClientCreateView.as_view(), name="new-client"),
]