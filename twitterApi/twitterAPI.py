import tweepy as tw
from dateutil import parser
import os

class TwitterAPI(object):

    def __init__(self, social_user=None):
        cruds = self.getCreds(social_user)
        auth = tw.OAuthHandler(cruds["twitter_key"], cruds["twitter_secret"])
        auth.set_access_token(cruds["token_key"], cruds["token_secret"])
        self.api = tw.API(auth, wait_on_rate_limit=True)
        self.account_id = cruds["account_id"]

    def getCreds(self, social_user):
        twitter_key = str(os.getenv('TWITTER_KEY'))
        twitter_secret = str(os.getenv('TWITTER_SECRET'))
        token_key = social_user.extra_data['access_token']['oauth_token']
        token_secret = social_user.extra_data['access_token']['oauth_token_secret']
        account_id = social_user.extra_data['id']
        obj = {"twitter_key":twitter_key, "twitter_secret":twitter_secret, "token_key":token_key, "token_secret": token_secret, "account_id": account_id}
        return obj
        
    def get_home_timeline(self):
        public_tweets = self.api.home_timeline()
        return public_tweets