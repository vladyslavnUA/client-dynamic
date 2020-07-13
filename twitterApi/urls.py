from django.urls import path, include
from . import views

app_name = 'twitter'

urlpatterns = [
    path('twitter/user/', views.ProfileView.as_view(), name='user-profile'),
    path('twitter/dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('post/tweet/', views.UpdateStatus, name='post-tweet'),
    path('post/retweet/<str:tweet_id>/', views.Retweet, name='retweet'),
    path('tweet/<str:tweet_id>/like', views.LikeTweet, name='like-tweet'),
    path('delete/tweet/<str:tweet_id>/', views.DeleteTweet, name='delete-tweet'),
]

