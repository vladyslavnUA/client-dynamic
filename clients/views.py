from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import (
    CreateView,
    UpdateView,
    DeleteView)
from django.contrib.auth.models import User
from django.shortcuts import render, HttpResponseRedirect, redirect
from django.urls import reverse, reverse_lazy
from .models import Client
from .forms import ClientForm

class IndexView(ListView):
    def get(self, request):
        context = {'data': 'self.getWeatherData()'}

        return render(request, "clients/index.html", context)

class ClienteleView(ListView):
    def get(self, request):
        user = User.objects.get(pk=request.user.id)
        clients = Client.objects.all()
        context = {"clients": clients}

        return render(request, "clients/clientele.html", context)

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

