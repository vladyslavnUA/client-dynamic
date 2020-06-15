from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

app_name = 'clients'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('dashboard/<str:page_token>/<str:page_id>', views.DashboardView.as_view(), name='dashboard'),
    path('user/', views.UserProfileView.as_view(), name='user-profile'),
    path('link/', views.LinkPageView.as_view(), name='link-page'),
    path('clientele/', views.ClienteleView.as_view(), name='clientele'),
    path('clientele/new', views.ClientCreateView.as_view(), name="new-client"),
    path('pages/', views.PagesView.as_view(), name="select-page"),
    path('pages/<str:page_name>/<str:token>/<int:page_id>', views.SinglePageView.as_view(), name="single-page"),
]