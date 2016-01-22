import facebook

from facebook_api_settings import * # holds short term access token, app id and app secret

graph = facebook.GraphAPI(access_token = access_token_s, version = '2.2') 

extended_token = graph.extend_access_token(app_id, app_secret)

print extended_token # valid for 60 days


