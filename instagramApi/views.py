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

# Create your views here.
class IndexView(ListView):
    

    def getPageInfo(self, graph, username, page_id, token):
        response = graph.get_object(page_id, fields="biography,followers_count,follows_count,id,ig_id,media_count,name,profile_picture_url,username,website,media{comments_count,like_count, shortcode}")
        

        return response

    def getComments(self, graph, media_id):
        
        data = graph.get_object(media_id+"/comments")

        print(data)
    
    # def getInsights(self, graph, page_id):

    #     data = graph.get_connections(id=page_id,
    #                                      connection_name='insights',
    #                                      metric='impressions, reach, follower_count, email_contacts, phone_call_clicks, text_message_clicks, get_directions_clicks, website_clicks, profile_views',
    #                                      date_preset='this_year',
    #                                      period='day',
    #                                      show_description_from_api_doc=True)

    #     for insight in data['data']:
    #         print("{} by {} | Description: {}".format(insight['name'], insight['period'], insight['description']))
    #         for value in insight['values']:
    #             print("Value: {}, Data: {}".format(value['value'], value['end_time']))
    #         print("----------------")

    def getImpressions(self, graph, page_id):
        today = datetime.datetime.today()
        lastMonth = today - datetime.timedelta(30)
        
        x = datetime.datetime(2020, 1, 1)
        y = datetime.datetime(2020, 1, 28)
        z = y - x


        today_stamp = today.strftime("%s")
        lastMonth_stamp = lastMonth.strftime("%s")

        data = graph.get_connections(id=page_id,
                                         connection_name='insights',
                                         metric='impressions, reach, follower_count, email_contacts, phone_call_clicks, text_message_clicks, get_directions_clicks, website_clicks, profile_views',
                                         date_preset='this_year',
                                         period='day',
                                         since=x, 
                                         until=y,
                                         show_description_from_api_doc=True)

        impressions = []
        reach = []
        profile_views = []
        engagement = []
        follower_count = []
        website_clicks = []

        for insight in data['data']:
            for value in insight['values']:
                    if insight['name'] == 'impressions':
                        impressions.append(value['value'])
                    elif insight['name'] == 'reach':
                        reach.append(value['value'])
                    elif insight['name'] == 'profile_views':
                        profile_views.append(value['value'])
                    elif insight['name'] == 'phone_call_clicks' or insight['name'] == 'phone_call_clicks' or insight['name'] == 'text_message_clicks':
                        engagement.append(value['value'])
                    elif insight['name'] == 'follower_count':
                        follower_count.append(value['value'])
                    elif insight['name'] == 'website_clicks':
                        website_clicks.append(value['value'])
                        # print("website_clicks")
                    # print(insight['name'])


        return impressions, reach, profile_views, engagement, follower_count, website_clicks


    def getMentions(self, graph, ig_id):
        # data = graph.get_object(ig_id, fields="mentioned_comment")


        # print(data)
        pass


    def get(self, request, username,  page_id, token):
        

        graph = facebook.GraphAPI(token)

        data = self.getPageInfo(graph, username, page_id, token)

        impressions, reach, profile_views, engagement, follower_count, website_clicks = self.getImpressions(graph, page_id)

        context = {'impressions': impressions, "reach": reach, "profile_views": profile_views, "engagement": engagement, "followers": follower_count, "website_clicks": website_clicks, "posts": data['media']['data']}




        return render(request, "instagramApi/dashboard.html", context)