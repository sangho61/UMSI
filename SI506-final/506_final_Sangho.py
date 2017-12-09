

import json
import webbrowser
from requests_oauthlib import OAuth2Session
from requests_oauthlib.compliance_fixes import facebook_compliance_fix
from your_app_data import APP_ID, APP_SECRET


# Set the Global facebook_session varible for FB access below
facebook_session = False

CACHE_FNAME = "facebook_cache.json"

try:
    f = open(CACHE_FNAME, "r")
    fstr = f.read()
    CACHE_DICTION = json.loads(fstr)
    f.close()
except:
    CACHE_DICTION = {}

def params_unique_combination(baseurl, params):
    alphabetized_keys = sorted(params.keys())
    res = []
    for k in alphabetized_keys:
        res.append("{}={}".format(k, params[k]))
    return baseurl +"?" + "&".join(res)

# Function for a request to Facebook.
def getFacebookPost(baseURL, params = {}):
    unique_ident = params_unique_combination(baseURL, params)
    if unique_ident in CACHE_DICTION:
        print("getting cached data...")
        return CACHE_DICTION[unique_ident]
    else:
        global facebook_session
        if not facebook_session:
            authorization_base_url =  'https://www.facebook.com/dialog/oauth'
            token_url = 'https://graph.facebook.com/oauth/access_token'
            redirect_uri = 'https://www.programsinformationpeople.org/runestone/oauth'

            scope = ['user_posts','pages_messaging','user_managed_groups','user_status','user_likes']
            facebook = OAuth2Session(APP_ID, redirect_uri=redirect_uri, scope=scope)
            facebook_session = facebook_compliance_fix(facebook)

            authorization_url, state = facebook_session.authorization_url(authorization_base_url)
            print('Opening browser to {} for authorization'.format(authorization_url))
            webbrowser.open(authorization_url)

            redirect_response = input('Paste the full redirect URL here: ')
            facebook_session.fetch_token(token_url, client_secret=APP_SECRET, authorization_response=redirect_response.strip())

        facebook_resp = facebook_session.get(baseURL, params=params)
        facebook_text = facebook_resp.text
        CACHE_DICTION[unique_ident] = json.loads(facebook_text)
        dumped_json_cache = json.dumps(CACHE_DICTION)
        fw = open(CACHE_FNAME,"w")
        fw.write(dumped_json_cache)
        fw.close()
        print(facebook_text)
        return CACHE_DICTION[unique_ident]




baseurl = 'https://graph.facebook.com/me/feed'
url_params = {}
url_params["fields"] = "message, likes, comments"
url_params["limit"] = 30

print(getFacebookPost(baseurl, params = url_params))


# class Post():
#     def __init__(self, post_dict={}):
#         if 'message' in post_dict:
#             self.message = post_dict['message']
#         else:
#             self.message = ''
#         if 'comments' in post_dict:
#             self.comments = post_dict['comments']['data']
#         else:
#             self.comments = []
#         if 'likes' in post_dict:
#             self.likes = post_dict['likes']['data']
#         else:
#             self.likes = []
#
#
#     def positive(self):
#         p=[]
#         p_num=0
#         for i in self.message.split():
#             if i in pos_ws:
#                 p_num += 1
#         return p_num
#
#
#     def negative(self):
#         n=[]
#         n_num=0
#         for i in self.message.split():
#             if i in neg_ws:
#                 n_num += 1
#         return n_num
#
#     def emo_score(self):
#         return self.positive() - self.negative()
