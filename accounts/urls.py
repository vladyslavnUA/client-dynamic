from django.urls import path
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from .views import SignUpView

app_name = 'accounts'

urlpatterns = [
    path('accounts/signup/', SignUpView.as_view(), name='signup'),
]
