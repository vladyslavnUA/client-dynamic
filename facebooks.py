# str(os.getenv('FACEBOOK_ACCESS_TOKEN'))
import requests, facebook, os

app_id = '859456564547837'
app_secret = '898f9c7d40e9b86aff1d708f7ee35236'
user_short_token = 'EAAMNq9M60P0BAGJRLC5OhAg1Czsy4q40kZAn1so8PvvSl77D1cEQxlhMrk1xFXjeyT0ZAdBmuoddmIQZCwvGjeZCdf7d3foIPJ76wbxPBTd8kqSh43FAeFzoNglDRUTNQOvpqozSPX585bIOZCIhCQWKwY7Ky6LrTgNFyTUJ3DtIIyNJ0U8b7JhVVrO4KwWcR3xbiijscZAQZDZD'
access_token_url = "https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id={}&client_secret={}&fb_exchange_token={}".format(app_id, app_secret, user_short_token)

r = requests.get(access_token_url)

access_token_info = r.json()
user_long_token = access_token_info['access_token']
graph = facebook.GraphAPI(access_token=user_long_token, 
                          version="3.1")

print(access_token_info)
pages_data = graph.get_object("/me/accounts")

print(pages_data)
# page id = 309647179589755
# curl -i -X GET "https://graph.facebook.com/309647179589755?fields=access_token&access_token=EAAMNq9M60P0BAGJRLC5OhAg1Czsy4q40kZAn1so8PvvSl77D1cEQxlhMrk1xFXjeyT0ZAdBmuoddmIQZCwvGjeZCdf7d3foIPJ76wbxPBTd8kqSh43FAeFzoNglDRUTNQOvpqozSPX585bIOZCIhCQWKwY7Ky6LrTgNFyTUJ3DtIIyNJ0U8b7JhVVrO4KwWcR3xbiijscZAQZDZD"