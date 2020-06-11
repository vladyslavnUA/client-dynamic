from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.shortcuts import render
import requests
import datetime
from dateutil import parser
# from .models import Mood
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from .models import Profile


class IndexView(ListView):
    def get(self, request):
        context = {'data': 'self.getWeatherData()'}

        return render(request, "clients/index.html", context)

class DashboardView(ListView):
    def get(self, request):
        return render(request, "clients/dashboard.html")

class UserProfileView(ListView):
    def get(self, request):
        user = User.objects.get(pk=request.user.id)

        name = False
        if user.last_name != "" and user.last_name != "":
            name = str(user.first_name)+" "+str(user.last_name)

        context = {"user": user, "name": name}
        
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
        return HttpResponseRedirect(reverse('clients:dashboard'))



