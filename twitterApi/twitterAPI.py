# import twitter
# from dateutil import parser

# class TwitterAPI(object):

#     def __init__(self, token, account_id=None):
#         self.tweet_ap = twitter.tweetAPI(token)
#         self.account_id = account_id

#     def get_insights(self):
#         page_insights = self.tweet_ap.get_connections(id=self.account_id,
#                                             connection_name='insights',
#                                             metric='impressions',
#                                             # date_preset='this_year',
#                                             # period='day',
#                                             show_description_from_api_doc=True)

#         tw_impressions = page_insights['data'][0]['values']

#         tw_impressions_nums = []

#         temp = None
#         sum = 0

#         for impression in tw_impressions:
#             datee = parser.parse(impression['end_time'])

#             if temp is None:
#                 temp = datee.month

#             if datee.month == temp:
#                 sum += impression['value']
#             else:
#                 tw_impressions_nums.append(sum)
#                 sum = 0
            
#             temp = datee.month

        
#         while len(tw_impressions_nums) < 12:
#             tw_impressions_nums.append(0)

#         return tw_impressions_nums
    
#     def get_engagements(self):
#         page_engagements = self.tweet_ap.get_connections(id=self.account_id,
#                                             connection_name='insights',
#                                             metric='engagements',
#                                             date_preset='totals',
#                                             # period='day',
#                                             show_description_from_api_doc=True)

#         tw_engagements = page_engagements['data'][0]['values']
#         tw_engagements_nums = []
#         temp = None
#         sum = 0
#         for eng in tw_engagements:
#             datee = parser.parse(eng['end_time'])

#             if temp is None:
#                 temp = datee
#             if datee.month == temp.month:
#                 sum += eng['value']
#             else:
#                 tw_engagements_nums.append(sum)
#                 sum = 0
            
#             temp = datee

#         while len(tw_engagements_nums) < 12:
#             tw_engagements_nums.append(0)

#         return tw_engagements_nums