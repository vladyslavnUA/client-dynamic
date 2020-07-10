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
        response = graph.get_object(page_id, fields="biography,followers_count,follows_count,id,ig_id,media_count,name,profile_picture_url,username,website,media{comments_count,like_count}")
        
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

        for insight in data['data']:
            for value in insight['values']:
                    if insight['name'] == 'impressions':
                        impressions.append(value['value'])
                    elif insight['name'] == 'reach':
                        reach.append(value['value'])
                    elif insight['name'] == 'profile_views':
                        profile_views.append(value['value'])


        return impressions, reach, profile_views





    def getMentions(self, graph, ig_id):
        # data = graph.get_object(ig_id, fields="mentioned_comment")


        # print(data)
        pass


    def get(self, request, username,  page_id, token):
        

        graph = facebook.GraphAPI(token)

        data = self.getPageInfo(graph, username, page_id, token)
        # print("Disvovery:\n________")
        # print("Profile Pic: {}\n________".format(data['profile_picture_url']))
        # print("Name: {}, Username: {}, ID: {}, IGID: {}".format(data['name'], data['username'], data['id'], data['ig_id']))
        # print("Biography: {}".format(data['biography']))
        # print("Website: {}".format(data['website']))
        # print("Followers: {}, Follows: {}, Media: {}\n________".format( data["followers_count"],data["follows_count"],data["media_count"]))
        # self.getMentions(graph, page_id)
        # print("_________")
        # print("Insights: ")
        # self.getInsights(graph, page_id)
        impressions, reach, profile_views = self.getImpressions(graph, page_id)
        # print("_________\nComments on Media:")
        # for media in data["media"]["data"]:
        #     print("ID: {}".format(media["id"]))
        #     print("Comments Count: {}".format(media["comments_count"]))
        #     self.getComments(graph, media['id'])
        #     print("Like Count: {}".format(media["like_count"]))
        # print("________")

        context = {'impressions': impressions, "reach": reach, "profile_views": profile_views}

        print(impressions)
        return render(request, "instagramApi/dashboard.html", context)