from django.urls import reverse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import (
    CreateView,
    UpdateView,
    DeleteView)
from django.shortcuts import render, HttpResponseRedirect
import os
import tweepy as tw
from clients.models import User
from twitterApi.twitterAPI import TwitterAPI

class ProfileView(ListView):



    def get(self, request):

        user = request.user
        


        return render(request, 'twitterApi/user.html')


    def post(self, request):
        user = User.objects.get(pk=request.user.id)
        # profile = Profile()


        user.first_name = request.POST.get("first_name")
        user.last_name = request.POST.get("last_name")
        user.email = request.POST.get("email")
        user.profile.company = request.POST.get("company")
        user.profile.bio = request.POST.get("bio")
        user.profile.role = request.POST.get("role")


        user.save()
        return HttpResponseRedirect(reverse('twitter:dashboard'))

def getCreds(social_user):
    twitter_key = str(os.getenv('TWITTER_KEY'))
    twitter_secret = str(os.getenv('TWITTER_SECRET'))
    token_key = social_user.extra_data['access_token']['oauth_token']
    token_secret = social_user.extra_data['access_token']['oauth_token_secret']
    obj = {"twitter_key":twitter_key, "twitter_secret":twitter_secret, "token_key":token_key, "token_secret": token_secret}
    return obj


class DashboardView(ListView):

    def get_sum(self, data):
        total = 0
        for i in data:
            total += i
        return total


    def get(self, request):
        user = request.user
        social_user = user.social_auth.get()

        api = TwitterAPI(social_user)

        context = {"tweets": api.get_home_timeline()}
        return render(request, 'twitterApi/dashboard.html', context)

def UpdateStatus(req):
    if req.method == 'POST':
        message=req.POST.get('message')
        user = req.user
        social_user = user.social_auth.get()
        
        api = TwitterAPI(social_user)
        api.post_status(message)

    return HttpResponseRedirect(reverse('twitter:dashboard'))