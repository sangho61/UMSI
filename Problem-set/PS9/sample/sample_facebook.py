import json
import webbrowser
import unittest
from requests_oauthlib import OAuth2Session # For accessing FB
from requests_oauthlib.compliance_fixes import facebook_compliance_fix # For accessing FB
from your_app_data import APP_ID, APP_SECRET

# Getting data from secret file so you don't share app data with the public/others/us, but do share code
APP_ID = APP_ID
APP_SECRET = APP_SECRET

facebook_session = False # For dealing with others' code for getting data from FB

# What does this function take as input?
# What type does it return? (CAREFUL)
def makeFacebookRequest(baseURL, params = {}):
    global facebook_session
    if not facebook_session:
        # OAuth endpoints given in the Facebook API documentation
        authorization_base_url = 'https://www.facebook.com/dialog/oauth'
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

    return facebook_session.get(baseURL, params=params)

baseurl = "https://graph.facebook.com/{}/feed".format("humansofnewyork")
# print(makeFacebookRequest(baseurl).text)
text_data_HNY = makeFacebookRequest(baseurl).text

python_thing = json.loads(text_data_HNY)
print(type(python_thing))
# What would you want to do next?

# or

params1 = {}
params1["fields"] = "message,comments,likes"
params1["limit"] = 10
msgcommentslikes_text_data_HNY = makeFacebookRequest(baseurl, params=params1).text # Don't forget -- what type does this function return?
python_stuff_msgcommentslikes = json.loads(msgcommentslikes_text_data_HNY)
print(type(python_stuff_msgcommentslikes))
print(python_stuff_msgcommentslikes.keys()) # What key looks interesting?
# Etc
print(python_stuff_msgcommentslikes["data"])
print(type(python_stuff_msgcommentslikes["data"])) # What's this? What's that stuff represent?
