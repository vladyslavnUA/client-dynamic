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

# print(access_token_info)
pages_data = graph.get_object("/me/accounts")

print(access_token_info)
print("__________________")

# getting all pages managed by account
pages_data = graph.get_object("/me/accounts")

page_id = pages_data['data'][0]['id']
page_name = pages_data['data'][0]['name']
page_category = pages_data['data'][0]['category']
page_tasks = pages_data['data'][0]['tasks']

print("{} ID# {} is {} tasked to {} contents".format(page_name, page_id, page_category, page_tasks))

print("______________________")

# getting specific information, in this case: about and category
page_id = '309647179589755'
page_token = None

for item in pages_data['data']:
    if item['id'] == page_id:
        page_token = item['access_token']
      
print('PAGE TOKEN: ' + page_token)

print(graph.get_object(id=page_id, fields='about, category'))
# page id = 309647179589755
# curl -i -X GET "https://graph.facebook.com/309647179589755?fields=access_token&access_token=EAAMNq9M60P0BAGJRLC5OhAg1Czsy4q40kZAn1so8PvvSl77D1cEQxlhMrk1xFXjeyT0ZAdBmuoddmIQZCwvGjeZCdf7d3foIPJ76wbxPBTd8kqSh43FAeFzoNglDRUTNQOvpqozSPX585bIOZCIhCQWKwY7Ky6LrTgNFyTUJ3DtIIyNJ0U8b7JhVVrO4KwWcR3xbiijscZAQZDZD"