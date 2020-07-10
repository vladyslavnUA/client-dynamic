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

class DashboardView(ListView):

    def get(self, request):
        user = request.user
        social_user = user.social_auth.get()
        twitter_key = str(os.getenv('TWITTER_KEY'))
        twitter_secret = str(os.getenv('TWITTER_SECRET'))

        token_key = social_user.extra_data['access_token']['oauth_token']
        token_secret = social_user.extra_data['access_token']['oauth_token_secret']


        auth = tw.OAuthHandler(twitter_key, twitter_secret)
        auth.set_access_token(token_key, token_secret)
        api = tw.API(auth, wait_on_rate_limit=True)

        public_tweets = api.home_timeline()
        
        for tweet in public_tweets:
            print("--------------------")
            # print(tweet.text)
            print(dir(tweet))
            print("--------------------")
            print(tweet.user)
            # print(tweet.source_url)
            break
    

        # user = api.get_user(user.username)

        # print(user.screen_name)
        # print(user.followers_count)
        # for friend in user.friends():
        #     print(friend.screen_name)

        # In this example, the handler is time.sleep(15 * 60),
# but you can of course handle it in any way you want.


        # for follower in tw.Cursor(api.followers).items():
        #     if follower.friends_count < 300:
        #         print(follower.screen_name)


        context = {"tweets": public_tweets}
        return render(request, 'twitterApi/dashboard.html', context)