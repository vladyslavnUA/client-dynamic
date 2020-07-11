from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import (
    CreateView,
    UpdateView,
    DeleteView)
import facebook
import requests
import json
import datetime

from linkedin_v2 import linkedin



# Create your views here.
class IndexView(ListView):

    def get(self, request):

        return render(request, "instagramApi/index.html", context)


class ProfileView(ListView):

    def makeApiCall(self, token, person_id):
        url = "https://api.linkedin.com/v2/me?oauth2_access_token={}".format(token)
    
        querystring = {'projection':"(id,firstName,lastName, profilePicture, vanityName)"}

        headers = {
            'oauth2_access_token': token,
            'projection': "(id,firstName,lastName, profilePicture, vanityName)"
            }

        response = requests.request("GET", url, headers=headers, params=querystring)

        print(response.text)

    def get(self, request):

        user = request.user
        social_user = user.social_auth.get()

        token = social_user.extra_data['access_token']

        application = linkedin.LinkedInApplication(token=token)



        profile = application.get_profile(member_id=1412421)
        # connections = application.get_connections()

        self.makeApiCall(token, social_user.extra_data['id'])

        return render(request, 'linkedinApi/user.html')


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
        return HttpResponseRedirect(reverse('linkedin:index'))
