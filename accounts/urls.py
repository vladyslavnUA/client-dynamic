from django.urls import path
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from .views import (
    SignUpView,
    UserProfile,
    ProfileUpdate,
#     ProfileDelete,
)

app_name = 'accounts'

urlpatterns = [
    path('signup/', SignUpView.as_view(), name="signup"),
    path('login/',
         auth_views.LoginView.as_view(template_name="accounts/login.html"),
         name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name="logout"),
    path('profiles/<int:pk>/update-profile/', ProfileUpdate.as_view(),
         name="update-profile"),
    path('profiles/<int:pk>/', UserProfile.as_view(), name="user-profile"),
]
