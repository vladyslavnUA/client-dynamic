from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import (
    CreateView,
    UpdateView,
    DeleteView)

from django.shortcuts import render

# Create your views here.
class IndexView(ListView):
    def get(self, request):
        context = {}
        return render(request, "bots/index.html", context)
