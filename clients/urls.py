from django.urls import path
from . import views

app_name = 'clients'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('dashboard', views.DashboardView.as_view(), name='dashboard'),
    path('user/', views.UserProfileView.as_view(), name='user-profile'),
    path('link/', views.LinkPageView.as_view(), name='link-page'),
    path('clientele/', views.ClienteleView.as_view(), name='clientele'),
    path('clientele/new', views.ClientCreateView.as_view(), name="new-client")
]