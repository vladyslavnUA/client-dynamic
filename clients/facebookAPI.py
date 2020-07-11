import facebook
from dateutil import parser

class FacebookAPI(object):

    def __init__(self, token, page_id=None):
        self.graph = facebook.GraphAPI(token)
        self.page_id = page_id

    def get_page_info(self, fields=None):
        if fields is None:
            return self.graph.get_object('me')
        else:
            return self.graph.get_object('me', fields=fields)

    def get_page_posts(self):
        posts = self.graph.get_object('me/posts', fields="about, story, message, created_time, shares, comments, permalink_url, id, actions")

        for post in posts['data']:
            post['created_time'] = parser.parse(post['created_time'])

        return posts['data']

    def get_pages(self):
        data = self.graph.get_object('me/accounts', fields='overall_star_rating,name,username, instagram_business_account,about,access_token,description,cover,picture')
        return data['data']

    def get_page_impressions_monthly(self):
        page_impressions = self.graph.get_connections(id=self.page_id,
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

    def get_page_likes_monthly(self):
        page_likes = self.graph.get_connections(id=self.page_id,
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

            else:
                fb_likes_nums.append(sum)
                sum = 0
            
            temp = datee.month

        
        while len(fb_likes_nums) < 12:
            fb_likes_nums.append(0)

        return fb_likes_nums

    def get_page_clicks_monthly(self):
        page_clicks = self.graph.get_connections(id=self.page_id,
                                            connection_name='insights',
                                            metric='page_total_actions',
                                            date_preset='this_year',
                                            period='day',
                                            show_description_from_api_doc=True)

        fb_clicks = page_clicks['data'][0]['values']
        fb_clicks_nums = []
        fb_clicks_months = []
        temp = None
        sum = 0
        for click in fb_clicks:
            datee = parser.parse(click['end_time'])
            if temp is None:
                temp = datee
            if datee.month == temp.month:
                sum += click['value']
            else:
                fb_clicks_nums.append(sum)
                fb_clicks_months.append(temp.month)
                sum = 0
            
            temp = datee

        while len(fb_clicks_nums) < 12:
            fb_clicks_nums.append(0)

        return fb_clicks_nums, fb_clicks_months

    def get_page_post_engagements(self):
        page_engagements = self.graph.get_connections(id=self.page_id,
                                            connection_name='insights',
                                            metric='page_post_engagements',
                                            date_preset='this_year',
                                            period='day',
                                            show_description_from_api_doc=True)

        fb_engagements = page_engagements['data'][0]['values']
        fb_engagements_nums = []
        fb_engagements_months = []
        temp = None
        sum = 0
        for eng in fb_engagements:
            datee = parser.parse(eng['end_time'])

            if temp is None:
                temp = datee
            if datee.month == temp.month:
                sum += eng['value']
            else:
                fb_engagements_nums.append(sum)
                fb_engagements_months.append(temp.month)
                sum = 0
            
            temp = datee

        while len(fb_engagements_nums) < 12:
            fb_engagements_nums.append(0)

        return fb_engagements_nums, fb_engagements_months

    def get_page_engagements(self):
        page_engaged_users = self.graph.get_connections(id=self.page_id,
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
                temp = datee
            if datee.month == temp.month:
                sum += eng['value']
            else:
                fb_engagements_nums.append(sum)
                sum = 0
            temp = datee


        while len(fb_engagements_nums) < 12:
            fb_engagements_nums.append(0)
        return fb_engagements_nums

    def get_page_reach(self):
        page_engaged_users = self.graph.get_connections(id=self.page_id,
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

    def page_positive_feedback_by_type(self):
        page_positive_feedback_by_type = self.graph.get_connections(id=self.page_id,
                                        connection_name='insights',
                                        metric='page_fans_locale',
                                        show_description_from_api_doc=True)
        feedbacks = page_positive_feedback_by_type['data']
        # fb_engagements_nums = []
        # temp = None
        # sum = 0
        # for feed in feedbacks:
        #     print(feed)
        #     datee = parser.parse(eng['end_time'])
        #     if temp is None:
        #         temp = datee.month
        #     if datee.month == temp:
        #         for k,v in eng['value'].items():
        #             sum += v
        #     else:
        #         fb_engagements_nums.append(sum)
        #         sum = 0
        #     temp = datee.month
        # while len(fb_engagements_nums) < 12:
        #     fb_engagements_nums.append(0)
        # return fb_engagements_nums

    def get_page_referrals(self):
        page_referrals = self.graph.get_connections(id=self.page_id,
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
    
    def post_to_facebook(self, message, url=None, link=None):
        
        if url is not None:
            print("posting image from api")
            self.graph.put_photo(image=open(url, 'rb'),message=message)
        elif link is not None:
            self.graph.put_object(
                    parent_object="me",
                    connection_name="feed",
                    message=message,
                    link=link,
                )
        else:
            self.graph.put_object(
                parent_object="me",
                connection_name="feed",
                message=message,
            )