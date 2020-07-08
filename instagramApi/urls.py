from django.urls import path, include
from . import views

app_name = 'instagram'

urlpatterns = [
    path('instagram/', views.IndexView.as_view(), name='index'),
]