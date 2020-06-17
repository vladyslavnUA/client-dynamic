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
import facebook
import json

class IndexView(ListView):
    def get(self, request):
        context = {'data': 'self.getWeatherData()'}

        return render(request, "clients/index.html", context)

        
class DashboardView(ListView):

    def get_page_impressions_monthly(self, graph, page_id):
        page_impressions = graph.get_connections(id=page_id,
                                         connection_name='insights',
                                         metric='page_impressions',
                                         date_preset='this_year',
                                         period='day',
                                         show_description_from_api_doc=True)

        fb_impressions = page_impressions['data'][0]['values']

        fb_impressions_nums = []

        temp = None
        sum = 0

        for impression in fb_impressions:
            datee = parser.parse(impression['end_time'])

            if temp is None:
                temp = datee.month

            if datee.month == temp:
                sum += impression['value']
            else:
                fb_impressions_nums.append(sum)
                sum = 0
            
            temp = datee.month

        
        while len(fb_impressions_nums) < 12:
            fb_impressions_nums.append(0)

        return fb_impressions_nums

    def get_page_likes_monthly(self, graph, page_id):
        page_likes = graph.get_connections(id=page_id,
                                         connection_name='insights',
                                         metric='page_positive_feedback_by_type',
                                         date_preset='this_year',
                                         period='day',
                                         show_description_from_api_doc=True)

        fb_likes = page_likes['data'][0]['values']

        fb_likes_nums = []

        temp = None
        sum = 0

        for like in fb_likes:
            datee = parser.parse(like['end_time'])

            if temp is None:
                temp = datee.month

            if datee.month == temp:

                sum += 1
                print(like['value'])


                # print('We are in month {}'.format(temp))
            else:
                fb_likes_nums.append(sum)
                sum = 0
                # print('NEXT MONTH {}'.format(datee.month))
            
            temp = datee.month

        
        while len(fb_likes_nums) < 12:
            fb_likes_nums.append(0)

        return fb_likes_nums
    
    def get_page_clicks_monthly(self, graph, page_id):
        page_clicks = graph.get_connections(id=page_id,
                                         connection_name='insights',
                                         metric='page_total_actions',
                                         date_preset='last_year',
                                         period='day',
                                         show_description_from_api_doc=True)

        fb_clicks = page_clicks['data'][0]['values']
        fb_clicks_nums = []
        temp = None
        sum = 0
        for click in fb_clicks:
            datee = parser.parse(click['end_time'])
            if temp is None:
                temp = datee.month
            if datee.month == temp:
                sum += click['value']
            else:
                fb_clicks_nums.append(sum)
                sum = 0
            
            temp = datee.month

        while len(fb_clicks_nums) < 12:
            fb_clicks_nums.append(0)

        return fb_clicks_nums

    def get_page_post_engagements(self, graph, page_id):
        page_engagements = graph.get_connections(id=page_id,
                                         connection_name='insights',
                                         metric='page_post_engagements',
                                         date_preset='this_year',
                                         period='day',
                                         show_description_from_api_doc=True)

        fb_engagements = page_engagements['data'][0]['values']
        fb_engagements_nums = []
        temp = None
        sum = 0
        for eng in fb_engagements:
            datee = parser.parse(eng['end_time'])

            if temp is None:
                temp = datee.month
            if datee.month == temp:
                sum += eng['value']
            else:
                fb_engagements_nums.append(sum)
                sum = 0
            
            temp = datee.month

        while len(fb_engagements_nums) < 12:
            fb_engagements_nums.append(0)

        return fb_engagements_nums

    def get_page_engagements(self, graph, page_id):
        page_engaged_users = graph.get_connections(id=page_id,
                                         connection_name='insights',
                                         metric='page_engaged_users',
                                         date_preset='this_year',
                                         period='day',
                                         show_description_from_api_doc=True)
        fb_engaged_users = page_engaged_users['data'][0]['values']
        fb_engagements_nums = []
        temp = None
        sum = 0
        for eng in fb_engaged_users:
            datee = parser.parse(eng['end_time'])
            if temp is None:
                temp = datee.month
            if datee.month == temp:
                sum += eng['value']
            else:
                fb_engagements_nums.append(sum)
                sum = 0
            temp = datee.month
        while len(fb_engagements_nums) < 12:
            fb_engagements_nums.append(0)
        return fb_engagements_nums

    def get_page_reach(self, graph, page_id):
        page_engaged_users = graph.get_connections(id=page_id,
                                        connection_name='insights',
                                        metric='page_impressions_frequency_distribution',
                                        date_preset='this_year',
                                        period='day',
                                        show_description_from_api_doc=True)
        fb_engaged_users = page_engaged_users['data'][0]['values']
        fb_engagements_nums = []
        temp = None
        sum = 0
        for eng in fb_engaged_users:
            # print(eng)
            datee = parser.parse(eng['end_time'])
            if temp is None:
                temp = datee.month
            if datee.month == temp:
                for k,v in eng['value'].items():
                    sum += v
            else:
                fb_engagements_nums.append(sum)
                sum = 0
            temp = datee.month
        while len(fb_engagements_nums) < 12:
            fb_engagements_nums.append(0)
        return fb_engagements_nums
    
    def get_page_referrals(self, graph, page_id):
        page_referrals = graph.get_connections(id=page_id,
                                        connection_name='insights',
                                        metric='page_fans_by_like_source_unique',
                                        date_preset='this_year',
                                        period='day',
                                        show_description_from_api_doc=True)
        fb_referrals = page_referrals['data'][0]['values']
        
        fb_referrals_nums = []
        temp = None
        sum = 0
        for eng in fb_referrals:

            print(eng)
            # print(eng)
            datee = parser.parse(eng['end_time'])
            if temp is None:
                temp = datee.month
            if datee.month == temp:
                for k,v in eng['value'].items():
                    sum += v
            else:
                fb_referrals_nums.append(sum)
                sum = 0
            temp = datee.month
        while len(fb_referrals_nums) < 12:
            fb_referrals_nums.append(0)
        return fb_referrals_nums

    # returns sum of an array
    def get_total(self, data):
        sum = 0
        for i in data:
            sum += i
        return sum


    def get(self, request, page_token, page_id):

        graph = facebook.GraphAPI(page_token)

        data = graph.get_object('me')


        fb_page_engaged_users = self.get_page_engagements(graph, page_id)
        fb_page_reach = self.get_page_reach(graph, page_id)
        fb_page_impressions = self.get_page_impressions_monthly(graph, page_id)
        fb_page_engagments = self.get_page_post_engagements(graph, page_id)
        fb_total_cta = self.get_page_clicks_monthly(graph, page_id)

        print(fb_page_engagments)

        posts = graph.get_object('me/posts', fields="about, story, message, created_time, shares, comments, permalink_url")

        for post in posts['data']:
            post['created_time'] = parser.parse(post['created_time'])

        print(data)

        context = {'page': data, "fb_p_eng_users": fb_page_engaged_users, "fb_page_reach": fb_page_reach, 
                    "fb_page_impressions": fb_page_impressions, "fb_page_engagments": fb_page_engagments, 
                    "total_page_engagments": self.get_total(fb_page_engagments), "fb_total_cta": fb_total_cta,
                    "total_cta": self.get_total(fb_total_cta), 'posts': posts['data']}
        return render(request, "clients/dashboard.html", context)

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

    def get(self, request):
        user = User.objects.get(pk=request.user.id)
        social_user = user.social_auth.get(provider="facebook")
        token = social_user.extra_data['access_token']

        if user.profile.fb_page_id != '' and user.profile.fb_page_token != '':
            return HttpResponseRedirect(reverse('clients:dashboard', kwargs={'page_token': user.profile.fb_page_token, 'page_id':user.profile.fb_page_id }))

        graph = facebook.GraphAPI(token)
        data = graph.get_object('me', fields='first_name, location, link, email, posts, picture')

        pages_data = graph.get_object('me/accounts', fields='overall_star_rating,name,about,access_token,description,cover,picture')        

        context = {'pages':  pages_data["data"]}



        return render(request, "clients/pages.html", context)

class SinglePageView(ListView):

    def get(self, request, token, page_id, page_name):

        user = User.objects.get(pk=request.user.id)
        user = user.social_auth.get(provider="facebook")



        graph = facebook.GraphAPI(token)
        posts = graph.get_object('{}/posts'.format(page_id), fields='id, message, actions')

        context = {'posts':  posts['data'], 'page_id': page_id, 'page_name': page_name, 'page_token': token}

        return render(request, "clients/single-page.html", context)

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