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
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from .models import Profile, Client
from .forms import ClientForm


class IndexView(ListView):
    def get(self, request):
        context = {'data': 'self.getWeatherData()'}

        return render(request, "clients/index.html", context)
        
class DashboardView(ListView):
    def get(self, request):
        user = User.objects.get(pk=request.user.id)
        return render(request, "clients/dashboard.html")

class ClienteleView(ListView):
    def get(self, request):
        user = User.objects.get(pk=request.user.id)
        return render(request, "clients/clientele.html")

class LinkPageView(ListView):
    def get(self, request):
        context = {'data': 'self.getWeatherData()'}

        return render(request, "clients/link-page.html", context)


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
        return HttpResponseRedirect(reverse('clients:link-page'))

class ClientCreateView(CreateView):
    model = Client
    form_class = ClientForm
    queryset = Client.objects.all()
    template_name = 'clients/client-form.html'
    
    def get(self, request):
        context = {'form': ClientForm()}
        return render(request, self.template_name, context)

    def create_client(request):
        # template_name = 'clients/client-form.html'
        heading_message = 'New Client Form'
        if request.method == 'GET':
            formset = ClientFormset(request.GET or None)
        elif request.method == 'POST':
            formset = ClientFormset(request.POST)
            if formset.is_valid():
                for form in formset:
                    # extract name from each form and save
                    name = form.cleaned_data.get('name')
                    email = form.cleaned_data.get('email')
                    address = form.cleaned_data.get('address')
                    # save book instance
                    if name:
                        Client(name=name).save()
                        Client(email=email).save()
                        Client(address=address).save()
                # once all books are saved, redirect to book list view
                return redirect('clientele')
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
        '''Ensures the user adding the Code is an officer.'''
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