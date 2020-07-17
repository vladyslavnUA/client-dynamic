from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import (
    CreateView,
    UpdateView,
    DeleteView)
import datetime
from dateutil import parser
from django.contrib.auth.models import User
from django.shortcuts import render, HttpResponseRedirect, HttpResponse, redirect
from django.urls import reverse, reverse_lazy
import facebook
from django.core.files.storage import FileSystemStorage
from .facebookAPI import FacebookAPI


class DashboardView(ListView):

    # returns sum of an array
    def get_sum(self, data):
        total = 0
        for i in data:
            total += i
        return total

    def get_fullName(self, user):
        name = False
        if user.last_name != "":
            name = str(user.first_name)
        if  user.last_name != "":
            name = " "+str(user.last_name)

        return name

    def get(self, request, page_token, page_id):
        user = User.objects.get(pk=request.user.id)
        social_user = user.social_auth.get(provider="facebook")

        graph = FacebookAPI(page_token, page_id)

        fb_page_engagments, fb_page_engagments_months = graph.get_page_post_engagements()
        fb_total_cta, fb_total_cta_months = graph.get_page_clicks_monthly()

        # graph.page_positive_feedback_by_type()

        context = {'page': graph.get_page_info(), "fb_p_eng_users": graph.get_page_engagements(),
                    "fb_page_reach": graph.get_page_reach(), "fb_page_impressions": graph.get_page_impressions_monthly(), 
                    "fb_page_engagments": fb_page_engagments, "fb_page_engagments_months": fb_page_engagments_months, 
                    "total_page_engagments": self.get_sum(fb_page_engagments), "fb_total_cta": fb_total_cta,
                    "fb_total_cta_months": fb_total_cta_months, "picture": social_user.extra_data["picture"]["data"]["url"],
                    "total_cta": self.get_sum(fb_total_cta), 'posts': graph.get_page_posts(), "name": self.get_fullName(user), 
                    "token": page_token
                    }

        return render(request, "facebookApi/dashboard.html", context)

def PostFacebook(req, page_token):
    user = User.objects.get(pk=req.user.id)
    graph = FacebookAPI(page_token)
   
    if req.method == 'POST':
        message=req.POST.get('message')
        location=req.POST.get('location')
        image=req.POST.get('image')
        link=req.POST.get('link')

        if image is not "":
            myfile = req.FILES['image']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            uploaded_file_url = fs.url(filename)
            graph.post_to_facebook(message, uploaded_file_url, link)

        else:
            graph.post_to_facebook(message, None, link)
    
    return HttpResponseRedirect(reverse('facebookApi:dashboard', kwargs={'page_token': user.profile.fb_page_token, 'page_id':user.profile.fb_page_id }))

class LinkPageView(ListView):
    def get(self, request):
        context = {'data': 'self.getWeatherData()'}

        return render(request, "facebookApi/link-page.html", context)

class PagesView(ListView):

    def get(self, request, show):
        user = User.objects.get(pk=request.user.id)
        social_user = user.social_auth.get(provider="facebook")
        token = social_user.extra_data['access_token']

        # if user.profile.fb_page_id != '' and user.profile.fb_page_token != '':
        #     return HttpResponseRedirect(reverse('clients:dashboard', kwargs={'page_token': user.profile.fb_page_token, 'page_id':user.profile.fb_page_id }))

        graph = FacebookAPI(token)
        data = graph.get_page_info('first_name, location, link, email, posts, picture')

        context = {'pages':  graph.get_pages(), "show": show}

        return render(request, "facebookApi/pages.html", context)

class SinglePageView(ListView):

    def get(self, request, token, page_id, page_name):

        user = User.objects.get(pk=request.user.id)
        user = user.social_auth.get(provider="facebook")

        graph = facebook.GraphAPI(token, page_id)

        context = {'posts':  graph.get_page_posts(), 'page_id': page_id, 'page_name': page_name, 'page_token': token}

        return render(request, "facebookApi/single-page.html", context)

class UserProfileView(ListView):
    def get(self, request):
        user = User.objects.get(pk=request.user.id)

        # print("-------------------")

        social_user = user.social_auth.get()
        social_use = social_user.extra_data.get('id')
        # token = social_user.extra_data['access_token']
        social_s = social_user.extra_data
        print("Social User: ", social_user)
        print("Social: ", social_s)
        
        if "twitter" == social_user.provider:
            return redirect('twitter:user-profile')
        elif "linkedin-oauth2" == social_user.provider:
            return redirect('linkedin:user-profile')
        

        name = False
        if user.last_name != "" and user.last_name != "":
            name = str(user.first_name)+" "+str(user.last_name)
        
        context = {"user": user, "name": name, "social_user": social_user.extra_data, "account_id": social_use }
        
        if 'picture' in social_user.extra_data:
            context['picture'] =  social_user.extra_data["picture"]["data"]["url"]
        
        
        return render(request, "facebookApi/user.html", context)

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
        return HttpResponseRedirect(reverse('facebookApi:link-page'))

def SaveFbPageView(req, page_token, page_id):
    user = User.objects.get(pk=req.user.id)


    user.profile.fb_page_id = page_id
    user.profile.fb_page_token = page_token

    user.save()

    return HttpResponseRedirect(reverse('facebookApi:dashboard', kwargs={'page_token': page_token, 'page_id':page_id }))