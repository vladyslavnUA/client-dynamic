from django.urls import reverse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import (
    CreateView,
    UpdateView,
    DeleteView)
from django.shortcuts import render, HttpResponseRedirect
import os, json
from clients.models import User
from twitterApi.twitterAPI import TwitterAPI
from django.core.files.storage import FileSystemStorage


class ProfileView(ListView):

    def get(self, request):

        user = request.user
        social_user = user.social_auth.get()

        api = TwitterAPI(social_user)

        user_info = api.get_user_info()


        context = {
            "picture": user_info["profile_image_url"],
            "name": user_info["name"],
            "bio": str(user_info["description"]),
        }


        return render(request, 'twitterApi/user.html', context)


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

    def get(self, request):
        user = request.user
        social_user = user.social_auth.get()
        api = TwitterAPI(social_user)
        # followers = api.get_followers_list()
        # incoming_friendships = api.get_incoming_friendships()
        # outgoing_friendships = api.get_outgoing_friendships()
        # api.get_lookup_friendships('screen_name,screen_name,screen_name' )
        # home_timeline = api.get_home_timeline(1)
        mentions_timeline = api.get_mentions_timeline(10)
        # user_timeline = api.get_user_timeline(10)
        # favorite_tweets = api.get_favorite_tweets()
        # like_tweet = api.like_tweet(tweet_id)
        # unlike_tweet = api.unlike_tweet(tweet_id)
        # retweets_of_me = api.retweets_of_me()


        user_info = api.get_user_info()
        
        print(json.dumps(user_info, indent=4), "\n")

        context = {"tweets": mentions_timeline, 'social_user': user_info}
        return render(request, 'twitterApi/dashboard.html', context)

def UpdateStatus(req):
    if req.method == 'POST':
        message=req.POST.get('message')
        image=req.POST.get('image')
        link=req.POST.get('link')
        user = req.user
        social_user = user.social_auth.get()
        api = TwitterAPI(social_user)

        uploaded_attachment_url = None
        if image is not "":
            attachment = req.FILES['image']
            fs = FileSystemStorage()
            filename = fs.save(attachment.name, attachment)
            uploaded_attachment_url = fs.url(filename)

        print(json.dumps(api.post_tweet(message, uploaded_attachment_url), indent=4))

    return HttpResponseRedirect(reverse('twitter:dashboard'))

def DeleteTweet(req, tweet_id):
    social_user = req.user.social_auth.get()
    api = TwitterAPI(social_user)
    print(api.delete_tweet(tweet_id))
    return HttpResponseRedirect(reverse('twitter:dashboard'))

def Retweet(req, tweet_id):
    social_user = req.user.social_auth.get()
    api = TwitterAPI(social_user)
    print(api.post_retweet(tweet_id))
    return HttpResponseRedirect(reverse('twitter:dashboard'))

def LikeTweet(req, tweet_id):
    social_user = req.user.social_auth.get()
    api = TwitterAPI(social_user)
    print(api.like_tweet(tweet_id))
    return HttpResponseRedirect(reverse('twitter:dashboard'))
