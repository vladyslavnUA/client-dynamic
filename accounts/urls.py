from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from accounts import views

# app_name = 'accounts'

urlpatterns = [
    path('accounts/signup/', views.SignUpView.as_view(), name='signup'),
    path('login/', views.login, name='login-social'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout-social'),
    path('social-auth/', include('social_django.urls', namespace='social')),
]
