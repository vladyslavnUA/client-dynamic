
from dateutil import parser
import os, requests, base64, random, time, json, hmac, hashlib, re
from escape import Escape as escape
from oauthlib.oauth1.rfc5849.signature import collect_parameters
from six.moves import urllib
from requests_oauthlib import OAuth1Session
import oauth2 as oauth
import woeid
from yahoo_oauth import OAuth1



class TwitterAPI(object):

    def __init__(self, social_user=None):
        self.cruds = self.getCreds(social_user)
        consumer = oauth.Consumer(self.cruds["twitter_key"], self.cruds["twitter_secret"])
        token = oauth.Token(self.cruds["token_key"], self.cruds["token_secret"])
        self.client = oauth.Client(consumer, token)
        self.get_trends()


    def post_tweet(self, message, image):
        post_tweet_url = "https://api.twitter.com/1.1/statuses/update.json"
        status = urllib.parse.quote(message)

        media_ids = ''
        if image is not None:
            media_ids = self.upload_media(image)

        resp, content = self.client.request(post_tweet_url+'?status='+ status+'&media_ids='+str(media_ids), "POST")
        # else:
        #     resp, content = self.client.request(post_tweet_url+'?status='+ status, "POST")

        return json.loads(content.decode('utf-8'))

    def delete_tweet(self, tweet_id):
        delete_url = "https://api.twitter.com/1.1/statuses/destroy/"+str(tweet_id)+".json"
        resp, content = self.client.request(delete_url+"?id="+str(tweet_id), "POST")
        return json.loads(content.decode('utf-8'))

    def post_retweet(self, tweet_id):
        delete_url = "https://api.twitter.com/1.1/statuses/retweet/"+str(tweet_id)+".json"
        resp, content = self.client.request(delete_url+"?id="+str(tweet_id), "POST")
        return json.loads(content.decode('utf-8'))

    def unlike_tweet(self, tweet_id):
        url = 'https://api.twitter.com/1.1/favorites/destroy.json'
        resp, content = self.client.request(url+"?id="+str(tweet_id), "POST")
        return json.loads(content.decode('utf-8'))

    def retweets_of_me(self, count=5):
        url = 'https://api.twitter.com/1.1/statuses/retweets_of_me.json'
        resp, content = self.client.request(url+"?count="+str(count), "GET")

        return json.loads(content.decode('utf-8'))

    def get_trends(self, location=None):
        pass

        # app_id = "dj0yJmk9ZlpaY0MyY1ZnQWVEJnM9Y29uc3VtZXJzZWNyZXQmc3Y9MCZ4PTJl"
        # text = "nyc"
        # yahoo = 'http://where.yahooapis.com/v1/places.q(\'%s\')?appid=%s&format=json' % (text, app_id)

        # r = requests.get(url)
        # jsondata = r.text

        # print(jsondata)
        # sfid = "ChIJIQBpAG2ahYAR_6128GcTUEo"
        # resp, content = self.client.request(url+"?id="+sfid)

        # data = json.loads(content.decode('utf-8'))
        
        # print(data)
        # for trends in data:
        #     for trend in trends['trends']:
        #         print("\n", json.dumps(trend['name'], indent=4))
        #         print(json.dumps(trend['url'], indent=4), "\n")
            
    def upload_media(self, filename):
        url_media = "https://upload.twitter.com/1.1/media/upload.json"
        url_text = "https://api.twitter.com/1.1/statuses/update.json"

        twitter = OAuth1Session(self.cruds["twitter_key"], self.cruds["twitter_secret"], self.cruds["token_key"], self.cruds["token_secret"])

        files = {"media" : open(filename, 'rb')}
        req_media = twitter.post(url_media, files = files)

        if req_media.status_code != 200:
            print ("image app fail: %s", req_media.text)
            exit()

        media_id = json.loads(req_media.text)['media_id']
        print ("Media ID: %d" % media_id)

        return media_id

    def get_home_timeline(self, count=5):
        home_timeline_url = 'https://api.twitter.com/1.1/statuses/home_timeline.json'
        resp, content = self.client.request(home_timeline_url+"?count="+str(count), "GET")
        return json.loads(content.decode('utf-8'))
    
    def get_mentions_timeline(self, count=5):
        home_timeline_url = 'https://api.twitter.com/1.1/statuses/mentions_timeline.json'
        resp, content = self.client.request(home_timeline_url+"?count="+str(count), "GET")
        return json.loads(content.decode('utf-8'))

    def get_favorite_tweets(self, count=5):
        url = "https://api.twitter.com/1.1/favorites/list.json"
        resp, content = self.client.request(url+"?count="+str(count), "GET")
        return json.loads(content.decode('utf-8'))

    def get_user_timeline(self, count=5):
        home_timeline_url = 'https://api.twitter.com/1.1/statuses/user_timeline.json'
        resp, content = self.client.request(home_timeline_url+"?count="+str(count), "GET")
        return json.loads(content.decode('utf-8'))

    def get_followers_list(self):
        
        show_user_url = 'https://api.twitter.com/1.1/followers/list.json'

        resp, content = self.client.request(show_user_url + '?user_id=' + str(self.cruds["user_id"]), "GET")

        return json.loads(content.decode('utf-8'))

        # available user fileds
        # https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/user-object
        # for user in response['users']:
        #     print(user['name'], "Location:" ,user['location'])

    def get_incoming_friendships(self):
        incoming_friendships_url = 'https://api.twitter.com/1.1/friendships/incoming.json'
        resp, content = self.client.request(incoming_friendships_url, "GET")
        return json.loads(content.decode('utf-8'))

    def get_outgoing_friendships(self):
        outgoing_friendships_url = 'https://api.twitter.com/1.1/friendships/outgoing.json'
        resp, content = self.client.request(outgoing_friendships_url, "GET")
        return json.loads(content.decode('utf-8'))

    def get_lookup_friendships(self, name):
        
        lookup_friendships_url = 'https://api.twitter.com/1.1/friendships/lookup.json'

        resp, content = self.client.request(lookup_friendships_url+'?screen_name='+name, "GET")

        return json.loads(content.decode('utf-8'))

    def get_user_info(self):
        
        show_user_url = 'https://api.twitter.com/1.1/users/show.json'

        resp, content = self.client.request(show_user_url + '?user_id=' + str(self.cruds["user_id"])+"&include_email=true", "GET")

        print(json.loads(content.decode('utf-8')))
        return json.loads(content.decode('utf-8'))













    def getCreds(self, social_user):
        cruds = {
            "twitter_key":str(os.getenv('TWITTER_KEY')),
            "twitter_secret":str(os.getenv('TWITTER_SECRET')),
            "token_key":social_user.extra_data['access_token']['oauth_token'],
            "token_secret": social_user.extra_data['access_token']['oauth_token_secret'],
            "user_id": social_user.extra_data['id'],
            "screen_name": social_user.extra_data['access_token']['screen_name']
            }
        # print(social_user.extra_data)
        return cruds

    




# def get_authorize(self):        
    #     request_token_url = "https://api.twitter.com/oauth/request_token"
    #     app_callback_url = "http://localhost:8000/twitter/callback/"

    #     consumer = oauth.Consumer(self.cruds["twitter_key"], self.cruds["twitter_secret"])
    #     client = oauth.Client(consumer)
    #     resp, content = client.request(request_token_url, "POST", body=urllib.parse.urlencode({
    #                                 "oauth_callback": app_callback_url}))

    #     request_token = dict(urllib.parse.parse_qsl(content))

    #     oauth_token = request_token[b'oauth_token'].decode('utf-8')
    #     oauth_token_secret = request_token[b'oauth_token_secret'].decode('utf-8')

    #     self.cruds["oauth_token_secret"] = oauth_token_secret
        
    #     return {"authorize_url": "https://api.twitter.com/oauth/authorize", 
    #             "oauth_token": oauth_token, 
    #             "request_token_url": request_token_url,
    #             "oauth_token_secret": oauth_token_secret
    #         }


        

    # def get_token(self):
    #     url = 'https://api.twitter.com/1.1/statuses/update.json' 
        # key_secret = '{}:{}'.format(self.cruds["twitter_key"], self.cruds["twitter_secret"]).encode('ascii')
        
        # twitter_key = base64.b64encode(self.cruds["twitter_key"])
        # twitter_key = twitter_key.decode('ascii')


        # print(self.get_nonce())


        # # nonce = base64.b64encode(System.Text.Encoding.UTF8.GetBytes(TimeInSecondsSince1970
        # #     + TimeInSecondsSince1970 + TimeInSecondsSince1970))
        # headers = {
        #     "include_entities": True,
        #     "oauth_consumer_key": self.cruds["twitter_key"],
        #     "oauth_nonce": self.get_nonce,

        #     'Authorization': 'Basic {}'.format(b64_encoded_key),
        #     'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
        # }


        # data = {
        #     'grant_type': 'client_credentials'
        # }

        # response = requests.post(url, headers=headers, data=data)
        
        # access_token = response.json()['access_token']

        # return access_token

    # def get_token_developer(self):
    #     url = 'https://api.twitter.com/oauth2/token'
        
    #     key_secret = '{}:{}'.format(self.cruds["twitter_key"], self.cruds["twitter_secret"]).encode('ascii')
    #     b64_encoded_key = base64.b64encode(key_secret)
    #     b64_encoded_key = b64_encoded_key.decode('ascii')

    #     headers = {
    #         'Authorization': 'Basic {}'.format(b64_encoded_key),
    #         'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
    #     }


    #     data = {
    #         'grant_type': 'client_credentials'
    #     }

    #     response = requests.post(url, headers=headers, data=data)
        
    #     access_token = response.json()['access_token']

    #     return access_token
