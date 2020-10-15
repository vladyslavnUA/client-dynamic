from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

app_name = 'facebook'

urlpatterns = [
    path('dashboard/<str:page_token>/<str:page_id>', views.DashboardView.as_view(), name='dashboard'),
    path('user/', views.UserProfileView.as_view(), name='user-profile'),
    path('link/', views.LinkPageView.as_view(), name='link-page'),
    path('pages/<int:show>', views.PagesView.as_view(), name="select-page"),
    path('save/pages/<str:page_token>/<str:page_id>', views.SaveFbPageView, name="save-fb-page"),
    path('pages/<str:page_name>/<str:token>/<int:page_id>', views.SinglePageView.as_view(), name="single-page"),
    path('pages/post/<str:page_token>', views.PostFacebook, name="post-to-facebook")
]