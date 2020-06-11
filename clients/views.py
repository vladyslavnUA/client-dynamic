from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.shortcuts import render
import requests
import datetime
from dateutil import parser
# from .models import Mood
from django.http import HttpResponseRedirect
from django.urls import reverse

class IndexView(ListView):
    def get(self, request):
        context = {'data': 'self.getWeatherData()'}

        return render(request, "clients/index.html", context)

class DashboardView(ListView):
    def get(self, request):
        return render(request, "clients/dashboard.html")

class UserProfileView(ListView):
    def get(self, request):
        context = {'data': 'self.getWeatherData()'}

        return render(request, "clients/user.html", context)
