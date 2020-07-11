from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import (
    CreateView,
    UpdateView,
    DeleteView)
from django.shortcuts import render, redirect
import requests
import datetime
from dateutil import parser
# from .models import Mood
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.models import User
from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from .models import Profile, Client
from .forms import ClientForm
import facebook
import json
import os
from django.core.files.storage import FileSystemStorage
from instagram.client import InstagramAPI
from .facebookAPI import FacebookAPI

class IndexView(ListView):
    def get(self, request):
        context = {'data': 'self.getWeatherData()'}

        return render(request, "clients/index.html", context)

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

        return render(request, "clients/dashboard.html", context)

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
    
    return HttpResponseRedirect(reverse('clients:dashboard', kwargs={'page_token': user.profile.fb_page_token, 'page_id':user.profile.fb_page_id }))

class ClienteleView(ListView):
    def get(self, request):
        user = User.objects.get(pk=request.user.id)
        clients = Client.objects.all()
        context = {"clients": clients}

        return render(request, "clients/clientele.html", context)

class LinkPageView(ListView):
    def get(self, request):
        context = {'data': 'self.getWeatherData()'}

        return render(request, "clients/link-page.html", context)

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

        return render(request, "clients/pages.html", context)

class SinglePageView(ListView):

    def get(self, request, token, page_id, page_name):

        user = User.objects.get(pk=request.user.id)
        user = user.social_auth.get(provider="facebook")

        graph = facebook.GraphAPI(token, page_id)

        context = {'posts':  graph.get_page_posts(), 'page_id': page_id, 'page_name': page_name, 'page_token': token}

        return render(request, "clients/single-page.html", context)

class UserProfileView(ListView):
    def get(self, request):
        user = User.objects.get(pk=request.user.id)

        # print("-------------------")
        u = user.social_auth.get()

        if "twitter" == u.provider:
            return redirect('twitter:user-profile')
        elif "linkedin-oauth2" == u.provider:
            return redirect('linkedin:user-profile')
        

        social_user = user.social_auth.get()

        name = False
        if user.last_name != "" and user.last_name != "":
            name = str(user.first_name)+" "+str(user.last_name)
        
        context = {"user": user, "name": name, "social_user": social_user.extra_data }
        
        if 'picture' in social_user.extra_data:
            context['picture'] =  social_user.extra_data["picture"]["data"]["url"]
        
        
        return render(request, "clients/user.html", context)

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
        return HttpResponseRedirect(reverse('clients:link-page'))

class ClientCreateView(CreateView):
    model = Client
    form_class = ClientForm
    queryset = Client.objects.all()
    template_name = 'clients/client-form.html'
    
    def get(self, request):
        form = ClientForm()
        context = {'form': form}

        print(context)
        return render(request, self.template_name, context)

    def post(self, request):
        if request.method == 'POST':
            form = ClientForm(request.POST)
            if form.is_valid():
                client = form.save()
                return redirect('clients:clientele')

        return render(request, template_name, {
            'formset': formset,
            'heading': heading_message,
        })

    def test_func(self):
        client = self.get_object()
        user = self.request.user
        return (user.is_authenticated is True)

class ClientUpdateView(UpdateView):
    model = Client
    form_class = ClientForm
    template_name = 'clients/client-update.html'
    queryset = Client.objects.all()

    def test_func(self):
        client = self.get_object()
        user = self.request.user
        return (user.is_authenticated is True)

class ClientDeleteView(DeleteView):

    model = Client
    # template_name = 'codes/crud/delete.html'
    success_url = reverse_lazy('clients:clientele')
    queryset = Client.objects.all()

    def test_func(self):
        client = self.get_object()
        user = self.request.user
        return (user.is_authenticated is True)

    def get(self, request, name):
        client = self.get_queryset().get(name=name)
        context = {
            'client': client
        }
        return render(request, context)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.save()
        return HttpResponseRedirect(success_url)

def SaveFbPageView(req, page_token, page_id):
    user = User.objects.get(pk=req.user.id)


    user.profile.fb_page_id = page_id
    user.profile.fb_page_token = page_token

    user.save()

    return HttpResponseRedirect(reverse('clients:dashboard', kwargs={'page_token': page_token, 'page_id':page_id }))