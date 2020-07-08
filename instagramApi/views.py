from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import (
    CreateView,
    UpdateView,
    DeleteView)

# Create your views here.
class IndexView(ListView):
    
    
    def get(self, request):
        context = {'data': 'self.getWeatherData()'}



        return render(request, "instagramApi/index.html", context)